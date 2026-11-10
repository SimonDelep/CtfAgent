"""Boucle principale RSI — variante **évolution des poids** (branche weight).

Différence avec la branche `dreamer` : au lieu de faire évoluer la *stratégie*
(texte) en prenant le meilleur du rêve, on fait évoluer les **poids**. La
stratégie `policy/v0` reste FIGÉE ; ce sont les versions de poids `weights/vN/`
qui changent.

    1. RÉEL      : l'agent ⑤ attaque les challenges d'entraînement avec la
                   version de poids courante (sandbox ③) ; arbres enregistrés ⑥.
    2. RÊVE      : le rêveur ⑧ rejoue les mauvaises bifurcations via le
                   simulateur ⑦.
    3. ENTRAÎNEMENT : l'entraîneur transforme les MEILLEURES trajectoires (chemin
                   gagnant vérifié + meilleurs rêves) en jeu d'entraînement et
                   produit une version de poids candidate v(n+1) (LoRA, base gelée).
    4. VALIDATION : la porte ⑩ compare la version courante et la candidate sur
                   l'ensemble de VALIDATION ; adoption seulement si meilleure.
    5. FINAL     : évaluation unique sur le TEST, jamais vu.

⚠️ Inversion assumée de l'invariant du README (« les poids ne changent jamais »).
Voir state.md pour les risques (contamination, surapprentissage, coût) et les
garde-fous (rejection sampling, base gelée, porte sur held-out).

Garde-fous d'exécution : `enable_sandbox=False` (aucun Docker) et
`enable_training=False` (aucun fine-tuning) par défaut → la boucle est
pilotable à sec.
"""
from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path

from core.agent import Agent
from core.forge import ToolForge
from core.llm import LLMClient
from core.loader import load_challenge
from core.sandbox import Sandbox
from core.tools import unregister_generated
from core.trainer import WeightTrainer
from core.tree import SearchTree
from core.types import Policy, RSIReport, WeightVersion
from dream.dreamer import Dreamer
from runner import evaluate as evaluate_mod
from runner import gate as gate_mod


# --------------------------------------------------------------------------- #
# Chargement de la stratégie FIGÉE
# --------------------------------------------------------------------------- #
def load_policy(policy_root: str | Path, version: str = "v0") -> Policy:
    """Charge la stratégie (figée ici) depuis `policy/<version>/`."""
    base = Path(policy_root) / version
    if not base.is_dir():
        raise FileNotFoundError(f"stratégie introuvable : {base}")

    def _read(p: Path) -> str:
        return p.read_text(encoding="utf-8") if p.is_file() else ""

    skills: dict[str, str] = {}
    if (base / "skills").is_dir():
        for f in sorted((base / "skills").glob("*.md")):
            skills[f.name] = _read(f)
    tools: dict[str, str] = {}
    if (base / "tools").is_dir():
        for f in sorted((base / "tools").glob("*.py")):
            tools[f.name] = _read(f)
    return Policy(version=version, path=base, prompt=_read(base / "prompt.md"),
                 heuristics=_read(base / "heuristics.md"), skills=skills, tools=tools)


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
@dataclass
class RSIConfig:
    policy_root: Path
    weights_root: Path
    workspace_root: Path
    db_path: Path
    base_ref: str
    train: list[Path] = field(default_factory=list)
    val: list[Path] = field(default_factory=list)
    test: list[Path] = field(default_factory=list)
    iterations: int = 3
    max_steps: int = 25
    enable_sandbox: bool = False
    enable_training: bool = False


# --------------------------------------------------------------------------- #
# L'orchestrateur (évolution des poids)
# --------------------------------------------------------------------------- #
class WeightRSIOrchestrator:
    """Chef d'orchestre de la boucle RSI qui fait évoluer les POIDS."""

    def __init__(self, config: RSIConfig, llm: LLMClient | None = None) -> None:
        self.cfg = config
        # Client « patron » : sert de gabarit (base_url, clé) ; le modèle servi
        # est choisi par version de poids via llm.with_model(...).
        self.base_llm = llm
        self.tree = SearchTree(config.db_path)
        self.forge = ToolForge(config.workspace_root / "forge" / "live")
        self.dreamer = Dreamer(self.tree)
        self.trainer = WeightTrainer(config.weights_root, config.base_ref,
                                     enabled=config.enable_training)
        self.policy = load_policy(config.policy_root, "v0")  # FIGÉE
        self._activate_policy_tools()
        self.report = RSIReport()

    # -- utilitaires ------------------------------------------------------ #
    def _activate_policy_tools(self) -> None:
        unregister_generated()
        self.forge.load_policy_tools(self.policy)

    def _llm_for(self, weights: WeightVersion) -> LLMClient | None:
        """Client LLM servant la version de poids donnée."""
        if self.base_llm is None:
            return None
        return self.base_llm.with_model(weights.model_ref)

    # -- 1. phase réelle -------------------------------------------------- #
    def real_phase(self, weights: WeightVersion) -> None:
        """L'agent attaque le train avec la version de poids courante."""
        llm = self._llm_for(weights)
        agent = Agent(llm, self.tree, max_steps=self.cfg.max_steps, forge=self.forge)
        for cdir in self.cfg.train:
            ws = self.cfg.workspace_root / cdir.name
            challenge = load_challenge(cdir, workspace=ws)
            sandbox = Sandbox(ws, enabled=self.cfg.enable_sandbox,
                              timeout=self.cfg.max_steps * 2, forge=self.forge)
            agent.run(challenge, self.policy, sandbox)

    # -- 2+3. rêve + entraînement ---------------------------------------- #
    def dream_and_train(self, base_weights: WeightVersion) -> WeightVersion:
        """Rejoue les bifurcations, bâtit le jeu d'entraînement, entraîne."""
        dreams = []
        for attempt in self.tree.solved_attempts():
            dreams.extend(self.dreamer.dream_attempt(attempt.id, attempt.challenge_name))
        examples = self.trainer.build_examples(self.tree, dreams)
        self.report.notes.append(
            f"{len(dreams)} rêve(s), {len(examples)} exemple(s) d'entraînement "
            f"depuis {base_weights.version}.")
        return self.trainer.train(base_weights, examples)

    # -- 4. validation ---------------------------------------------------- #
    def validate(self, base_weights: WeightVersion, candidate: WeightVersion):
        base_eval = self._evaluate(base_weights, self.cfg.val, scope="val-base")
        cand_eval = self._evaluate(candidate, self.cfg.val, scope="val-candidate")
        verdict = gate_mod.decide(base_eval, cand_eval)
        self.report.gate_history.append(verdict)
        return verdict

    # -- boucle complète -------------------------------------------------- #
    def run(self, start_version: str = "v0") -> RSIReport:
        weights = self.trainer.load_version(start_version)
        self.report.adopted_versions.append(weights.version)
        self.real_phase(weights)

        for _ in range(self.cfg.iterations):
            self.report.iterations += 1
            candidate = self.dream_and_train(weights)

            # Entraînement à sec / sans exemple → candidate == base : rien à valider.
            if candidate.is_base:
                self.report.notes.append(
                    f"{candidate.version} identique à la base "
                    f"(entraînement désactivé ou sans donnée) ; arrêt.")
                shutil.rmtree(candidate.path, ignore_errors=True)
                break

            verdict = self.validate(weights, candidate)
            if verdict.adopted:
                weights = candidate
                self.report.adopted_versions.append(weights.version)
                self.real_phase(weights)
            else:
                shutil.rmtree(candidate.path, ignore_errors=True)

        if self.cfg.test:
            self.report.final_eval = self._evaluate(weights, self.cfg.test, scope="test")
        return self.report

    # -- évaluation ------------------------------------------------------- #
    def _evaluate(self, weights: WeightVersion, dirs: list[Path], *, scope: str):
        ws = self.cfg.workspace_root / scope
        return evaluate_mod.evaluate(
            self.policy, dirs,
            llm=self._llm_for(weights), tree=self.tree, workspace_root=ws,
            enable_sandbox=self.cfg.enable_sandbox, max_steps=self.cfg.max_steps,
            forge=self.forge,
        )

    def close(self) -> None:
        self.tree.close()


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _discover(db_root: Path) -> list[Path]:
    return sorted(p.parent for p in db_root.rglob("challenge.json"))


def main(argv: list[str] | None = None) -> int:
    import argparse
    import sys

    root = Path(__file__).resolve().parent.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    parser = argparse.ArgumentParser(
        description="Boucle RSI — évolution des poids (branche weight)")
    parser.add_argument("--db", default=str(root / "CSAW26_LLMAC_DB"))
    parser.add_argument("--policy-root", default=str(root / "policy"))
    parser.add_argument("--weights-root", default=str(root / "weights"))
    parser.add_argument("--workspace-root", default=str(root / "data" / "ws"))
    parser.add_argument("--db-path", default=str(root / "data" / "trees.db"))
    parser.add_argument("--base-ref", default="huihui_ai/qwen3.5-abliterated:122b")
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--start", default="v0")
    parser.add_argument("--enable-sandbox", action="store_true")
    parser.add_argument("--enable-training", action="store_true",
                        help="autorise le fine-tuning réel (infra requise)")
    parser.add_argument("--no-llm", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    all_challenges = _discover(Path(args.db))
    n = len(all_challenges)
    train = all_challenges[: int(n * 0.6)]
    val = all_challenges[int(n * 0.6): int(n * 0.8)]
    test = all_challenges[int(n * 0.8):]

    if args.dry_run or n == 0:
        print(f"Challenges découverts : {n}")
        print(f"  train={len(train)} val={len(val)} test={len(test)}")
        print(f"  sandbox={'ON' if args.enable_sandbox else 'OFF'} "
              f"training={'ON' if args.enable_training else 'OFF'} "
              f"llm={'OFF' if args.no_llm else 'ON'}")
        if n == 0:
            print("Aucun challenge : initialise le sous-module CSAW26_LLMAC_DB.")
        return 0

    llm = None if args.no_llm else LLMClient()
    cfg = RSIConfig(
        policy_root=Path(args.policy_root),
        weights_root=Path(args.weights_root),
        workspace_root=Path(args.workspace_root),
        db_path=Path(args.db_path),
        base_ref=args.base_ref,
        train=train, val=val, test=test,
        iterations=args.iterations,
        enable_sandbox=args.enable_sandbox,
        enable_training=args.enable_training,
    )
    orch = WeightRSIOrchestrator(cfg, llm)
    report = orch.run(args.start)
    orch.close()

    print(f"Itérations : {report.iterations}")
    print(f"Versions de poids adoptées : {' → '.join(report.adopted_versions)}")
    for g in report.gate_history:
        print(f"  porte : {g.reason}")
    for note in report.notes:
        print(f"  · {note}")
    if report.final_eval:
        fe = report.final_eval
        print(f"Évaluation finale ({fe.policy_version}) : "
              f"{fe.solved}/{fe.total} flags, {fe.total_steps} étapes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

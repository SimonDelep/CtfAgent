"""Boucle principale RSI — **l'orchestrateur** du projet.

C'est la pièce qui coordonne tout le README :

    1. RÉEL      : l'agent ⑤ attaque les challenges d'entraînement (sandbox ③) ;
                   chaque tentative est enregistrée dans l'arbre ⑥.
    2. RÊVE      : sur les challenges résolus, le rêveur ⑧ rejoue les mauvaises
                   bifurcations via le simulateur ⑦.
    3. RÉFLEXION : le réflecteur ⑨ transforme les rêves en une stratégie
                   candidate v(n+1).
    4. VALIDATION: la porte ⑩ n'adopte la candidate que si elle fait mieux sur
                   l'ensemble de validation.
    5. On répète 2–4, puis une ÉVALUATION FINALE unique sur l'ensemble de test
       (CSAW 2026), jamais utilisé pour rêver.

Les poids du modèle ne changent jamais : seule la stratégie (`policy/vN/`)
évolue. L'orchestrateur ne lance aucune exécution Docker tant que
`enable_sandbox=False` : il est donc importable et pilotable à sec.
"""
from __future__ import annotations

# Permet `python3 runner/rsi_loop.py` autant que `python3 -m runner.rsi_loop` :
# on garantit que la racine du projet est dans le chemin d'import avant de
# charger le paquet `core`.
import sys as _sys
from pathlib import Path as _Path

_ROOT = _Path(__file__).resolve().parent.parent
if str(_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_ROOT))

import shutil
from dataclasses import dataclass, field
from pathlib import Path

from core.agent import Agent
from core.forge import ToolForge
from core.llm import LLMClient
from core.loader import load_challenge
from core.sandbox import Sandbox
from core.tools import unregister_generated
from core.trace import Tracer, get_tracer, set_tracer
from core.tree import SearchTree
from core.types import Candidate, Policy, RSIReport
from dream.dreamer import Dreamer
from dream.reflector import Reflector
from runner import evaluate as evaluate_mod
from runner import gate as gate_mod


# --------------------------------------------------------------------------- #
# Chargement / sauvegarde de stratégie ④
# --------------------------------------------------------------------------- #
def load_policy(policy_root: str | Path, version: str) -> Policy:
    """Charge une stratégie depuis `policy/<version>/`."""
    base = Path(policy_root) / version
    if not base.is_dir():
        raise FileNotFoundError(f"stratégie introuvable : {base}")
    prompt = _read(base / "prompt.md")
    heuristics = _read(base / "heuristics.md")
    skills: dict[str, str] = {}
    skills_dir = base / "skills"
    if skills_dir.is_dir():
        for f in sorted(skills_dir.glob("*.md")):
            skills[f.name] = _read(f)
    # Outils forgés portés par cette version (option 2).
    tools: dict[str, str] = {}
    tools_dir = base / "tools"
    if tools_dir.is_dir():
        for f in sorted(tools_dir.glob("*.py")):
            tools[f.name] = _read(f)
    return Policy(version=version, path=base, prompt=prompt,
                 heuristics=heuristics, skills=skills, tools=tools)


def save_candidate(policy_root: str | Path, base_policy: Policy, candidate: Candidate) -> Policy:
    """Écrit la candidate dans `policy/<nouvelle_version>/` et la renvoie chargée."""
    root = Path(policy_root)
    dst = root / candidate.version
    # On part d'une copie de la stratégie de base, puis on applique les éditions.
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(base_policy.path, dst)
    for edit in candidate.edits:
        target = dst / (edit.target if edit.target.endswith(".md") else f"{edit.target}.md")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(edit.new_content, encoding="utf-8")
    return load_policy(root, candidate.version)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


# --------------------------------------------------------------------------- #
# Configuration de la boucle
# --------------------------------------------------------------------------- #
@dataclass
class RSIConfig:
    policy_root: Path
    workspace_root: Path
    db_path: Path
    train: list[Path] = field(default_factory=list)
    val: list[Path] = field(default_factory=list)
    test: list[Path] = field(default_factory=list)
    iterations: int = 3
    max_steps: int = 25
    # Garde-fou : tant que False, aucune commande Docker n'est exécutée.
    enable_sandbox: bool = True


# --------------------------------------------------------------------------- #
# L'orchestrateur
# --------------------------------------------------------------------------- #
class RSIOrchestrator:
    """Chef d'orchestre de la boucle Dream-RSI."""

    def __init__(self, config: RSIConfig, llm: LLMClient | None = None) -> None:
        self.cfg = config
        self.llm = llm
        self.tree = SearchTree(config.db_path)
        # Forgeron d'outils (option 2), partagé par l'agent et la sandbox.
        self.forge = ToolForge(config.workspace_root / "forge" / "live")
        self.agent = Agent(llm, self.tree, max_steps=config.max_steps, forge=self.forge)
        self.dreamer = Dreamer(self.tree)
        # Noms de challenges (train+val+test) à bannir des stratégies.
        names = [p.name for p in (config.train + config.val + config.test)]
        self.reflector = Reflector(llm, challenge_names=names)
        self.report = RSIReport()

    # -- 1. phase réelle -------------------------------------------------- #
    def _activate_policy_tools(self, policy: Policy) -> None:
        """Rend disponibles les outils forgés portés par `policy`."""
        unregister_generated()  # repart du jeu de base
        n = self.forge.load_policy_tools(policy)
        if n:
            self.report.notes.append(f"{n} outil(s) forgé(s) chargé(s) depuis {policy.version}.")

    def real_phase(self, policy: Policy) -> None:
        """L'agent attaque les challenges d'entraînement ; arbres enregistrés."""
        get_tracer().set_phase("RÉEL", f"stratégie {policy.version}, "
                                       f"{len(self.cfg.train)} challenge(s)")
        self._activate_policy_tools(policy)
        for cdir in self.cfg.train:
            ws = self.cfg.workspace_root / cdir.name
            challenge = load_challenge(cdir, workspace=ws)
            sandbox = Sandbox(ws, enabled=self.cfg.enable_sandbox,
                              timeout=self.cfg.max_steps * 2, forge=self.forge)
            self.agent.run(challenge, policy, sandbox)

    # -- 2+3. rêve + réflexion ------------------------------------------- #
    def dream_and_reflect(self, policy: Policy) -> Candidate:
        """Rejoue les mauvaises bifurcations et propose une candidate v(n+1)."""
        get_tracer().set_phase("RÊVE", f"depuis {policy.version}")
        dreams = []
        for attempt in self.tree.solved_attempts():
            dreams.extend(self.dreamer.dream_attempt(attempt.id, attempt.challenge_name))
        self.report.notes.append(f"{len(dreams)} rêve(s) générés depuis {policy.version}.")
        return self.reflector.reflect(policy, dreams)

    # -- 4. validation ---------------------------------------------------- #
    def validate(self, baseline: Policy, candidate_policy: Policy):
        """Évalue baseline et candidate sur l'ensemble de validation, puis tranche."""
        base_eval = self._evaluate(baseline, self.cfg.val, scope="val-baseline")
        cand_eval = self._evaluate(candidate_policy, self.cfg.val, scope="val-candidate")
        verdict = gate_mod.decide(base_eval, cand_eval)
        self.report.gate_history.append(verdict)
        # Gate verdict goes to the global log
        get_tracer().set_phase("PORTE", f"{baseline.version} vs {candidate_policy.version}")
        get_tracer().event("gate", verdict.reason)
        return verdict

    # -- boucle complète -------------------------------------------------- #
    def run(self, start_version: str = "v0") -> RSIReport:
        """Lance la boucle RSI et renvoie le rapport."""
        policy = load_policy(self.cfg.policy_root, start_version)
        self.report.adopted_versions.append(policy.version)

        # Phase réelle une fois (remplit l'arbre). On peut la relancer après
        # chaque adoption pour exploiter la nouvelle stratégie ; ici une fois
        # suffit pour la structure de la boucle.
        self.real_phase(policy)

        for _ in range(self.cfg.iterations):
            self.report.iterations += 1
            get_tracer().set_phase(f"ITÉRATION {self.report.iterations}/{self.cfg.iterations}")
            candidate = self.dream_and_reflect(policy)
            # Option 2 : promouvoir les outils forgés utiles dans la candidate.
            # Ils seront ensuite validés par la porte ⑩ comme le reste.
            tool_edits = self.forge.promotable_edits(self.tree)
            if tool_edits:
                candidate.edits.extend(tool_edits)
                self.report.notes.append(
                    f"{len(tool_edits)} outil(s) forgé(s) proposé(s) à l'adoption.")
            if not candidate.edits:
                self.report.notes.append("Aucune édition proposée ; arrêt anticipé.")
                break
            candidate_policy = save_candidate(self.cfg.policy_root, policy, candidate)
            verdict = self.validate(policy, candidate_policy)
            if verdict.adopted:
                policy = candidate_policy
                self.report.adopted_versions.append(policy.version)
                self.real_phase(policy)  # réexploite avec la stratégie adoptée
            else:
                # Candidate rejetée : on efface sa version du disque.
                shutil.rmtree(candidate_policy.path, ignore_errors=True)

        # 5. évaluation finale unique sur le test, jamais vu.
        if self.cfg.test:
            self.report.final_eval = self._evaluate(policy, self.cfg.test, scope="test")
        return self.report

    # -- utilitaires ------------------------------------------------------ #
    def _evaluate(self, policy: Policy, dirs: list[Path], *, scope: str):
        ws = self.cfg.workspace_root / scope
        get_tracer().set_phase(scope.upper(), f"stratégie {policy.version}, "
                                              f"{len(dirs)} challenge(s)")
        # Active les outils forgés propres à CETTE stratégie avant de l'évaluer.
        self._activate_policy_tools(policy)
        return evaluate_mod.evaluate(
            policy, dirs,
            llm=self.llm, tree=self.tree, workspace_root=ws,
            enable_sandbox=self.cfg.enable_sandbox, max_steps=self.cfg.max_steps,
            forge=self.forge,
        )

    def close(self) -> None:
        self.tree.close()


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _discover(db_root: Path) -> list[Path]:
    """Liste les dossiers contenant un challenge.json sous un répertoire."""
    return sorted(p.parent for p in db_root.rglob("challenge.json"))


def main(argv: list[str] | None = None) -> int:
    import argparse
    import sys

    root = Path(__file__).resolve().parent.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    parser = argparse.ArgumentParser(description="Boucle RSI (orchestrateur CtfAgent)")
    parser.add_argument("--db", default=str(root / "CSAW26_LLMAC_DB"),
                        help="racine de la base de challenges")
    parser.add_argument("--policy-root", default=str(root / "policy"))
    parser.add_argument("--workspace-root", default=str(root / "data" / "ws"))
    parser.add_argument("--db-path", default=str(root / "data" / "trees.db"))
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--start", default="v0")
    parser.add_argument("--enable-sandbox", action="store_true",
                        help="autorise l'exécution Docker réelle (sinon à sec)")
    parser.add_argument("--no-llm", action="store_true")
    parser.add_argument("--quiet", action="store_true",
                        help="pas d'affichage console (les journaux sont tout de même écrits)")
    parser.add_argument("--log-root", default=str(root / "data" / "logs"),
                        help="dossier racine des journaux par challenge")
    parser.add_argument("--dry-run", action="store_true",
                        help="affiche la configuration et la liste des challenges, puis quitte")
    args = parser.parse_args(argv)

    all_challenges = _discover(Path(args.db))
    # Découpe simple train/val/test : à remplacer par un split explicite réel.
    n = len(all_challenges)
    train = all_challenges[: int(n * 0.6)]
    val = all_challenges[int(n * 0.6): int(n * 0.8)]
    test = all_challenges[int(n * 0.8):]

    if args.dry_run or n == 0:
        print(f"Challenges découverts : {n}")
        print(f"  train={len(train)} val={len(val)} test={len(test)}")
        print(f"  sandbox={'ON' if args.enable_sandbox else 'OFF (à sec)'} "
              f"llm={'OFF' if args.no_llm else 'ON'}")
        if n == 0:
            print("Aucun challenge : initialise le sous-module CSAW26_LLMAC_DB.")
        return 0

    # One log folder per run: data/logs/<date-time>/<challenge>.log|.jsonl
    import time
    log_dir = Path(args.log_root) / time.strftime("%Y%m%d-%H%M%S")
    set_tracer(Tracer(log_dir=log_dir, console=not args.quiet))
    print(f"Journaux : {log_dir}")

    llm = None if args.no_llm else LLMClient()
    cfg = RSIConfig(
        policy_root=Path(args.policy_root),
        workspace_root=Path(args.workspace_root),
        db_path=Path(args.db_path),
        train=train, val=val, test=test,
        iterations=args.iterations,
        enable_sandbox=args.enable_sandbox,
    )
    orch = RSIOrchestrator(cfg, llm)
    report = orch.run(args.start)
    orch.close()

    print(f"Itérations : {report.iterations}")
    print(f"Versions adoptées : {' → '.join(report.adopted_versions)}")
    for g in report.gate_history:
        print(f"  porte : {g.reason}")
    if report.final_eval:
        fe = report.final_eval
        print(f"Évaluation finale ({fe.policy_version}) : "
              f"{fe.solved}/{fe.total} flags, {fe.total_steps} étapes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

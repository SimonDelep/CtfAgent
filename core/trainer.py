"""Entraîneur de poids (branche weight) — on apprend en modifiant les poids.

Remplace le couple réflecteur ⑨ + sauvegarde de stratégie de la branche
`dreamer`. Au lieu de transformer les rêves en éditions de texte, on en fait un
**jeu d'entraînement** (les meilleures trajectoires) et on produit une nouvelle
**version de poids** candidate, validée ensuite par la porte ⑩.

Principe inversé par rapport au README : ici les poids évoluent, la stratégie
(`policy/v0`) reste figée.

⚠️ Deux garde-fous majeurs :
  1. **Rejection sampling strict** : on n'entraîne que sur des trajectoires
     VÉRIFIÉES gagnantes (chemin menant au vrai flag) et sur les meilleurs rêves
     qui rejoignent ce chemin. Jamais un flag rêvé, jamais une étape perdante.
     Cela limite la triche/contamination (voir discussion dans state.md).
  2. **Entraînement désactivé par défaut** (`enabled=False`). Le fine-tuning réel
     (LoRA, base gelée) dépend d'une infra absente ici : sans elle, l'entraîneur
     tourne « à sec » et renvoie une version identique au modèle de base (donc
     non adoptée par la porte). Le point d'extension est `_run_finetune`.

Versionnement comme la stratégie : `weights/vN/manifest.json` (+ `dataset.jsonl`).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from core.types import TrainingExample, WeightVersion

MAX_EXAMPLES = 2000


def _bump_version(version: str) -> str:
    m = re.match(r"v(\d+)", version)
    n = int(m.group(1)) + 1 if m else 1
    return f"v{n}"


class WeightTrainer:
    """Construit des exemples et produit des versions de poids candidates."""

    def __init__(
        self,
        weights_root: str | Path,
        base_ref: str,
        *,
        enabled: bool = False,
    ) -> None:
        self.weights_root = Path(weights_root)
        self.weights_root.mkdir(parents=True, exist_ok=True)
        self.base_ref = base_ref
        self.enabled = enabled

    # -- versions -------------------------------------------------------- #
    def load_version(self, version: str) -> WeightVersion:
        base = self.weights_root / version
        manifest = base / "manifest.json"
        if manifest.is_file():
            d = json.loads(manifest.read_text(encoding="utf-8"))
            return WeightVersion(
                version=version,
                path=base,
                base_ref=d.get("base_ref", self.base_ref),
                model_ref=d.get("model_ref", self.base_ref),
                adapter_path=d.get("adapter_path"),
                meta=d.get("meta", {}),
            )
        # v0 implicite = modèle de base gelé.
        base.mkdir(parents=True, exist_ok=True)
        wv = WeightVersion(version=version, path=base, base_ref=self.base_ref,
                           model_ref=self.base_ref)
        self._write_manifest(wv, n_examples=0)
        return wv

    def _write_manifest(self, wv: WeightVersion, *, n_examples: int) -> None:
        (wv.path / "manifest.json").write_text(json.dumps({
            "version": wv.version,
            "base_ref": wv.base_ref,
            "model_ref": wv.model_ref,
            "adapter_path": wv.adapter_path,
            "n_examples": n_examples,
            "meta": wv.meta,
        }, indent=2, ensure_ascii=False), encoding="utf-8")

    # -- construction du jeu d'entraînement ------------------------------ #
    def build_examples(self, tree, dreams) -> list[TrainingExample]:
        """Rejection sampling : trajectoires gagnantes + meilleurs rêves.

        Pour chaque tentative résolue, on rejoue le chemin gagnant et on crée un
        exemple (contexte → action correcte) par étape. Les rêves à score élevé
        qui rejoignent le chemin apportent des exemples supplémentaires, pondérés.
        """
        examples: list[TrainingExample] = []

        for attempt in tree.solved_attempts():
            if attempt.solution_leaf_id is None:
                continue
            path = tree.path_to_root(attempt.solution_leaf_id)
            transcript: list[str] = []
            for node in path:
                if node.action is None:
                    continue
                prompt = "\n".join(transcript) if transcript else "(début)"
                completion = json.dumps(
                    {"hypothesis": node.hypothesis, "tool": node.action.tool,
                     "args": node.action.args},
                    ensure_ascii=False,
                )
                examples.append(TrainingExample(
                    prompt=prompt, completion=completion, source="real-solution"))
                transcript.append(f"ACTION: {completion}")
                if node.observation is not None:
                    transcript.append(f"OBS: {node.observation.output[:500]}")

        # Meilleurs rêves qui rejoignent le chemin gagnant.
        good_dreams = sorted(
            (d for d in dreams if d.rejoined_solution_path and d.lesson.strip()),
            key=lambda d: d.score, reverse=True,
        )
        for d in good_dreams[:50]:
            examples.append(TrainingExample(
                prompt=f"Situation de blocage (challenge généralisé).",
                completion=d.lesson.strip(),
                source="dream",
                weight=min(2.0, 0.5 + d.score),
            ))

        return examples[:MAX_EXAMPLES]

    # -- entraînement ---------------------------------------------------- #
    def train(self, base: WeightVersion, examples: list[TrainingExample]) -> WeightVersion:
        """Produit une version de poids candidate à partir des exemples.

        Si l'entraînement est désactivé ou qu'il n'y a pas d'exemples, renvoie
        une candidate IDENTIQUE au modèle de base (la porte ne l'adoptera pas).
        """
        cand_version = _bump_version(base.version)
        cand_path = self.weights_root / cand_version
        cand_path.mkdir(parents=True, exist_ok=True)

        # Trace le jeu d'entraînement (utile même à sec, pour audit / repro).
        self._dump_dataset(cand_path / "dataset.jsonl", examples)

        if not self.enabled or not examples:
            reason = "entraînement désactivé" if not self.enabled else "aucun exemple"
            cand = WeightVersion(
                version=cand_version, path=cand_path,
                base_ref=base.base_ref, model_ref=base.model_ref,  # inchangé
                adapter_path=None,
                meta={"note": f"candidate à sec ({reason})", "n_examples": len(examples)},
            )
            self._write_manifest(cand, n_examples=len(examples))
            return cand

        # Entraînement réel : LoRA sur base gelée. À brancher selon l'infra.
        adapter = self._run_finetune(base, examples, cand_path)
        model_ref = adapter.get("model_ref", base.model_ref)
        cand = WeightVersion(
            version=cand_version, path=cand_path,
            base_ref=base.base_ref, model_ref=model_ref,
            adapter_path=adapter.get("adapter_path"),
            meta={"n_examples": len(examples), **adapter.get("meta", {})},
        )
        self._write_manifest(cand, n_examples=len(examples))
        return cand

    def _run_finetune(self, base: WeightVersion, examples, out_dir: Path) -> dict:
        """Point d'extension : lance un fine-tuning LoRA et renvoie l'adaptateur.

        TODO (infra requise) : entraîner un adaptateur LoRA sur `examples` avec la
        base `base.base_ref` GELÉE, fusionner/servir le résultat sous un
        `model_ref` dédié (ex. créer un modèle Ollama à partir d'un Modelfile, ou
        charger l'adaptateur côté vLLM), et renvoyer :
            {"model_ref": "<nom servi>", "adapter_path": "<chemin>", "meta": {...}}

        Tant que ce n'est pas branché, on lève une erreur explicite : activer
        `enabled=True` sans fournir l'infra est une mauvaise configuration.
        """
        raise NotImplementedError(
            "Fine-tuning réel non branché : implémente _run_finetune (LoRA, base "
            "gelée) puis sers le résultat sous un model_ref dédié."
        )

    def _dump_dataset(self, path: Path, examples: list[TrainingExample]) -> None:
        with path.open("w", encoding="utf-8") as fh:
            for ex in examples:
                fh.write(json.dumps({
                    "prompt": ex.prompt, "completion": ex.completion,
                    "source": ex.source, "weight": ex.weight,
                }, ensure_ascii=False) + "\n")

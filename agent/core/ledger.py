"""Ledger persistant : suivi des challenges tentés/résolus, pour reprendre sans tout refaire.

Fichier unique `agent/runs/ledger.json` : clé = "categorie/nom_dossier".
Un challenge est considéré "fait" (à sauter à la reprise) s'il a été résolu :
  - avec vérité-terrain : flag correct ;
  - sans vérité-terrain : un flag grounded a été accepté.
Les échecs restent "à refaire" (non sautés). `--force` ignore le ledger.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class Ledger:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data: dict[str, dict] = {}
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001 - ledger corrompu : on repart proprement
                self.data = {}

    @staticmethod
    def key(category: str, dirname: str) -> str:
        return f"{category}/{dirname}"

    def is_done(self, category: str, dirname: str) -> bool:
        e = self.data.get(self.key(category, dirname))
        if not e:
            return False
        # "fait" = résolu et (flag correct, ou correct inconnu mais solved en mode compét')
        return bool(e.get("solved") and e.get("correct") is not False)

    def get(self, category: str, dirname: str) -> dict | None:
        return self.data.get(self.key(category, dirname))

    def update(self, category: str, dirname: str, result, run_dir: Path) -> None:
        self.data[self.key(category, dirname)] = {
            "challenge": self.key(category, dirname),
            "solved": bool(getattr(result, "solved", False)),
            "correct": getattr(result, "correct", None),
            "flag": getattr(result, "flag", None),
            "steps": getattr(result, "steps", None),
            "tokens": getattr(result, "tokens", None),
            "forged_tools": getattr(result, "forged_tools", None),
            "reason": getattr(result, "reason", None),
            "run_dir": str(run_dir),
            "updated": datetime.now().isoformat(timespec="seconds"),
        }
        self._flush()

    def _flush(self) -> None:
        tmp = self.path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(self.path)  # écriture atomique

    def summary(self) -> str:
        if not self.data:
            return "(ledger vide)"
        rows = ["| Challenge | Fait | Flag | Steps | Tokens | MAJ |", "|---|---|---|---|---|---|"]
        for k in sorted(self.data):
            e = self.data[k]
            done = "oui" if (e.get("solved") and e.get("correct") is not False) else "non"
            rows.append(f"| {k} | {done} | {e.get('flag') or '-'} | {e.get('steps','-')} | "
                        f"{e.get('tokens','-')} | {e.get('updated','-')} |")
        return "\n".join(rows)

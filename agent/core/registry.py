"""Registre d'outils : fusionne outils NATIFS (base + méta-forge) et outils FORGÉS (fichiers).

- Natifs : handlers Python dans le process hôte (accès à l'executor/verifier/forge).
- Forgés : fichiers `.py` (SCHEMA + main(args)) exécutés via l'executor local.
Le registre expose la liste `tools` (format OpenAI) et un dispatch unifié.
"""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Callable


class ToolRegistry:
    def __init__(self):
        self._native: dict[str, dict] = {}        # name -> {"schema":..., "handler":...}
        self._forged: dict[str, dict] = {}        # name -> {"schema":..., "path":Path}
        self._forge_dirs: list[Path] = []

    # --- natifs ----------------------------------------------------------
    def register_native(self, schema: dict, handler: Callable[[dict, object], dict]) -> None:
        self._native[schema["name"]] = {"schema": schema, "handler": handler}

    # --- forgés ----------------------------------------------------------
    def add_forge_dir(self, path: Path) -> None:
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        if path not in self._forge_dirs:
            self._forge_dirs.append(path)

    def reload_forged(self) -> None:
        """Rescanne les dossiers de forge et recharge les schémas (hot-reload)."""
        self._forged.clear()
        for d in self._forge_dirs:
            for f in sorted(d.glob("*.py")):
                schema = _extract_schema(f)
                if schema and "name" in schema:
                    # un outil d'un dossier plus récent (par-run) écrase celui de lib/
                    self._forged[schema["name"]] = {"schema": schema, "path": f}

    # --- vue LLM ---------------------------------------------------------
    def schemas(self) -> list[dict]:
        out = []
        for entry in list(self._native.values()) + list(self._forged.values()):
            out.append({"type": "function", "function": entry["schema"]})
        return out

    def names(self) -> list[str]:
        return list(self._native) + list(self._forged)

    def describe(self) -> list[dict]:
        rows = []
        for name, e in self._native.items():
            rows.append({"name": name, "kind": "base", "description": e["schema"].get("description", "")})
        for name, e in self._forged.items():
            rows.append({"name": name, "kind": "forgé", "description": e["schema"].get("description", "")})
        return rows

    def is_forged(self, name: str) -> bool:
        return name in self._forged

    # --- dispatch --------------------------------------------------------
    def dispatch(self, name: str, args: dict, ctx) -> dict:
        if name in self._native:
            return self._native[name]["handler"](args, ctx)
        if name in self._forged:
            path = self._forged[name]["path"]
            return ctx.executor.run_forged(path, args)
        return {"error": f"outil inconnu: {name}", "available": self.names()}


def _extract_schema(path: Path) -> dict | None:
    """Lit la valeur de SCHEMA sans exécuter main() : on évalue le module top-level."""
    try:
        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src)
        # on n'exécute QUE les assignations top-level de SCHEMA (pas de main()).
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Name) and tgt.id == "SCHEMA":
                        return ast.literal_eval(node.value)
    except Exception:  # noqa: BLE001
        return None
    return None

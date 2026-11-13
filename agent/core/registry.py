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
        self._forged: dict[str, dict] = {}        # name -> {"schema":..., "path":Path} : ACTIF (exposé au LLM)
        self._library: dict[str, dict] = {}       # name -> {"schema":..., "path":Path} : BIBLIOTHÈQUE (sur demande)
        self._activated: set[str] = set()         # outils de bibliothèque tirés dans l'actif via load_tool
        self._forge_dirs: list[tuple[Path, bool]] = []   # (dossier, is_library)

    # --- natifs ----------------------------------------------------------
    def register_native(self, schema: dict, handler: Callable[[dict, object], dict]) -> None:
        self._native[schema["name"]] = {"schema": schema, "handler": handler}

    # --- forgés ----------------------------------------------------------
    def add_forge_dir(self, path: Path, library: bool = False) -> None:
        """Dossier scanné pour les outils forgés. library=True → catalogue (non exposé par défaut)."""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        if not any(p == path for p, _ in self._forge_dirs):
            self._forge_dirs.append((path, library))

    def reload_forged(self) -> None:
        """Rescanne les dossiers (hot-reload). Les outils du run sont ACTIFS ; ceux de la
        bibliothèque partagée restent en catalogue, sauf s'ils ont été activés (load_tool)."""
        self._forged.clear()
        self._library.clear()
        for d, is_lib in self._forge_dirs:
            for f in sorted(d.glob("*.py")):
                schema = _extract_schema(f)
                if not (schema and "name" in schema):
                    continue
                name = schema["name"]
                if is_lib:
                    self._library[name] = {"schema": schema, "path": f}
                else:
                    self._forged[name] = {"schema": schema, "path": f}
        # un outil de bibliothèque explicitement activé rejoint l'actif (s'il n'est pas déjà
        # masqué par un outil du run portant le même nom).
        for name in self._activated:
            if name not in self._forged and name in self._library:
                self._forged[name] = self._library[name]

    # --- bibliothèque (sur demande) -------------------------------------
    def search_library(self, query: str = "", limit: int = 15) -> list[dict]:
        """Catalogue des outils de bibliothèque NON encore actifs, filtré par mots-clés."""
        q = (query or "").lower().strip()
        toks = q.split()
        rows = []
        for name, e in self._library.items():
            if name in self._forged:   # déjà actif → inutile de le proposer
                continue
            desc = e["schema"].get("description", "")
            hay = f"{name} {desc}".lower()
            if not toks or any(t in hay for t in toks):
                rows.append({"name": name, "description": desc})
        rows.sort(key=lambda r: r["name"])
        return rows[:limit]

    def activate(self, name: str) -> bool:
        """Tire un outil de la bibliothèque dans l'actif (exposé au LLM, appelable)."""
        if name in self._forged:
            return True
        if name in self._library:
            self._activated.add(name)
            self._forged[name] = self._library[name]
            return True
        return False

    def library_count(self) -> int:
        return len([n for n in self._library if n not in self._forged])

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
        if name in self._library:   # filet : appel direct d'un outil de biblio non encore activé
            self.activate(name)
            return ctx.executor.run_forged(self._library[name]["path"], args)
        return {"error": f"outil inconnu: {name}", "available": self.names(),
                "hint": "cherche dans la bibliothèque avec search_tools puis load_tool."}


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

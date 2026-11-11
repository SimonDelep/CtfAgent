"""La FORGE : le LLM crée/modifie ses propres outils à la volée quand il est bloqué.

Un outil forgé est un fichier `.py` :
    SCHEMA = {...}            # construit par la forge à partir de name/description/parameters
    def main(args): ...       # écrit par le LLM ; print() = observation renvoyée
    if __name__ == "__main__": ...   # footer standard ajouté par la forge

forge_tool / edit_tool / list_tools sont exposés au LLM comme des outils natifs.
Validation : syntaxe compilée + présence de main(). En cas d'erreur, le message est renvoyé
au LLM pour qu'il corrige. Après succès : hot-reload du registre -> appelable au tour suivant.
"""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

from .registry import ToolRegistry

_NAME_RE = re.compile(r"^[a-z][a-z0-9_]{1,40}$")

_FOOTER = (
    "\n\nif __name__ == \"__main__\":\n"
    "    import json as _json, sys as _sys\n"
    "    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}\n"
    "    main(_args)\n"
)


class Forge:
    def __init__(self, registry: ToolRegistry, run_forge_dir: Path, lib_dir: Path, shared_lib: bool = True):
        self.registry = registry
        self.run_forge_dir = Path(run_forge_dir)
        self.lib_dir = Path(lib_dir)
        self.run_forge_dir.mkdir(parents=True, exist_ok=True)
        self.lib_dir.mkdir(parents=True, exist_ok=True)
        self.target_dir = self.lib_dir if shared_lib else self.run_forge_dir
        # les deux dossiers sont scannés ; l'outil le plus spécifique (par-run) l'emporte
        registry.add_forge_dir(self.lib_dir)
        registry.add_forge_dir(self.run_forge_dir)
        registry.reload_forged()

    # --- construction / validation --------------------------------------
    def _build_source(self, name: str, description: str, parameters: dict, code: str) -> str:
        schema = {"name": name, "description": description, "parameters": parameters}
        header = f"SCHEMA = {json.dumps(schema, ensure_ascii=False, indent=2)}\n\n"
        return header + code.rstrip() + _FOOTER

    def _validate(self, name: str, source: str) -> str | None:
        if not _NAME_RE.match(name):
            return "nom invalide : minuscules/chiffres/_ , 2-41 caractères, commence par une lettre."
        if name in ("run_shell", "run_python", "read_file", "copy_challenge_file",
                    "submit_flag", "forge_tool", "edit_tool", "list_tools"):
            return f"'{name}' est un outil réservé : choisis un autre nom."
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            return f"erreur de syntaxe: {exc}"
        has_main = any(isinstance(n, ast.FunctionDef) and n.name == "main" for n in tree.body)
        if not has_main:
            return "le code doit définir une fonction top-level `def main(args):`."
        try:
            compile(source, name, "exec")
        except Exception as exc:  # noqa: BLE001
            return f"compilation échouée: {exc}"
        return None

    def _write(self, name: str, source: str) -> Path:
        path = self.target_dir / f"{name}.py"
        path.write_text(source, encoding="utf-8")
        self.registry.reload_forged()
        return path

    # --- handlers exposés au LLM ----------------------------------------
    def forge_tool(self, args, ctx):
        name = str(args.get("name", "")).strip()
        description = str(args.get("description", "")).strip()
        parameters = args.get("parameters") or {"type": "object", "properties": {}}
        if isinstance(parameters, str):
            try:
                parameters = json.loads(parameters)
            except json.JSONDecodeError as exc:
                return {"ok": False, "error": f"`parameters` n'est pas un JSON valide: {exc}"}
        code = args.get("code", "")
        if not code.strip():
            return {"ok": False, "error": "`code` vide : fournis le corps de `def main(args):`."}
        source = self._build_source(name, description, parameters, code)
        err = self._validate(name, source)
        if err:
            return {"ok": False, "error": err}
        path = self._write(name, source)
        return {"ok": True, "message": f"outil '{name}' forgé et disponible au prochain tour.",
                "path": str(path)}

    def edit_tool(self, args, ctx):
        name = str(args.get("name", "")).strip()
        entry = self.registry._forged.get(name)
        if not entry:
            return {"ok": False, "error": f"'{name}' n'est pas un outil forgé modifiable.",
                    "forged": [n for n in self.registry._forged]}
        code = args.get("code", "")
        if not code.strip():
            return {"ok": False, "error": "`code` vide."}
        schema = entry["schema"]
        # autorise la mise à jour optionnelle de description/parameters
        description = str(args.get("description", schema.get("description", ""))).strip()
        parameters = args.get("parameters", schema.get("parameters", {"type": "object", "properties": {}}))
        if isinstance(parameters, str):
            try:
                parameters = json.loads(parameters)
            except json.JSONDecodeError as exc:
                return {"ok": False, "error": f"`parameters` invalide: {exc}"}
        source = self._build_source(name, description, parameters, code)
        err = self._validate(name, source)
        if err:
            return {"ok": False, "error": err}
        # réécrit dans le dossier d'origine de l'outil
        path = Path(entry["path"])
        path.write_text(source, encoding="utf-8")
        self.registry.reload_forged()
        return {"ok": True, "message": f"outil '{name}' modifié.", "path": str(path)}

    def list_tools(self, args, ctx):
        return {"ok": True, "tools": self.registry.describe()}

    # --- enregistrement des méta-outils ---------------------------------
    def register_meta_tools(self) -> None:
        self.registry.register_native({
            "name": "forge_tool",
            "description": ("Crée un NOUVEL outil réutilisable quand les outils actuels ne suffisent pas. "
                            "Fournis le corps de `def main(args):` ; utilise print() pour renvoyer le résultat. "
                            "L'outil devient appelable au tour suivant."),
            "parameters": {"type": "object", "properties": {
                "name": {"type": "string", "description": "nom en snake_case (minuscules)."},
                "description": {"type": "string", "description": "ce que fait l'outil (vu par le LLM)."},
                "parameters": {"type": "object", "description": "JSON schema des arguments (type object)."},
                "code": {"type": "string", "description": "corps Python définissant `def main(args):`."},
            }, "required": ["name", "description", "code"]},
        }, self.forge_tool)

        self.registry.register_native({
            "name": "edit_tool",
            "description": "Modifie un outil déjà forgé (corrige/améliore son code).",
            "parameters": {"type": "object", "properties": {
                "name": {"type": "string"},
                "code": {"type": "string"},
                "description": {"type": "string"},
                "parameters": {"type": "object"},
            }, "required": ["name", "code"]},
        }, self.edit_tool)

        self.registry.register_native({
            "name": "list_tools",
            "description": "Liste tous les outils disponibles (base + forgés) avec leur description.",
            "parameters": {"type": "object", "properties": {}},
        }, self.list_tools)

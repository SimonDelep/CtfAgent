"""Forgeron d'outils (option 2) — l'agent fabrique ses propres outils.

Quand l'agent résolveur bloque, il peut appeler le tool méta `create_tool` pour
écrire un nouvel outil réutilisable. Ce module :

  - **valide** le code proposé (syntaxe + contrat `run(args)` + garde-fou) ;
  - l'**emballe** dans un script autonome exécuté en mode isolé (`python3 -I`) ;
  - le **persiste** dans un magasin d'outils vivants (`data/forge/live/`) ;
  - l'**enregistre** pour qu'il soit utilisable immédiatement et à l'avenir.

⚠️ Sécurité : le code forgé est écrit par le LLM. Il n'est **JAMAIS exécuté sur
l'hôte** — uniquement dans la sandbox Docker ③ (`--network none`, magasin monté
en lecture seule). Le forgeron ne fait qu'écrire des fichiers ; l'exécution
passe toujours par `core.sandbox.Sandbox`. Un filtre statique rejette en plus
quelques motifs manifestement destructeurs (défense en profondeur).

Persistance versionnée comme la stratégie : les outils retenus sont promus dans
`policy/v(n+1)/tools/` par la boucle RSI, puis validés par la porte ⑩.
"""
from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from core.tools import BUILTIN_NAMES, ToolSpec, get_tool, register_tool
from core.types import PolicyEdit

# Motifs refusés même si l'exécution est sandboxée (défense en profondeur).
_DENY_PATTERNS = [
    r"\brm\s+-rf\s+/",
    r"shutil\.rmtree\s*\(\s*['\"]?/",
    r":\(\)\s*\{",            # fork bomb
    r"\bmkfs\b",
    r"/etc/(passwd|shadow)",
    r"\bos\.fork\b",
]

_NAME_RE = re.compile(r"^[a-z][a-z0-9_]{1,40}$")
_META_PREFIX = "# CTFAGENT_TOOL_META: "


@dataclass
class ForgeResult:
    ok: bool
    message: str
    name: str | None = None


@dataclass
class ForgedMeta:
    description: str = ""
    args: dict[str, str] = field(default_factory=dict)


class ToolForge:
    """Gère le cycle de vie des outils forgés."""

    def __init__(self, live_dir: str | Path = "data/forge/live") -> None:
        self.live_dir = Path(live_dir)
        self.live_dir.mkdir(parents=True, exist_ok=True)
        # Chemin du magasin tel que monté dans le conteneur.
        self.container_mount = "/forge"

    # -- création (appelé par l'agent via create_tool) -------------------- #
    def forge(self, name: str, description: str, args, code: str) -> ForgeResult:
        name = (name or "").strip()
        if not _NAME_RE.match(name):
            return ForgeResult(False, f"nom invalide '{name}' (attendu [a-z][a-z0-9_]…).")
        if name in BUILTIN_NAMES:
            return ForgeResult(False, f"'{name}' est un tool de base, choisis un autre nom.")
        if not isinstance(args, dict):
            args = {}

        ok, why = self._validate(code)
        if not ok:
            return ForgeResult(False, f"code refusé : {why}")

        file_text = self._wrap(name, description, args, code)
        (self.live_dir / f"{name}.py").write_text(file_text, encoding="utf-8")
        self._register(name, description, args)
        return ForgeResult(True, f"outil '{name}' forgé et disponible.", name=name)

    # -- validation statique --------------------------------------------- #
    def _validate(self, code: str) -> tuple[bool, str]:
        if not code or not code.strip():
            return False, "code vide."
        for pat in _DENY_PATTERNS:
            if re.search(pat, code):
                return False, f"motif interdit détecté (/{pat}/)."
        try:
            tree = ast.parse(code)
        except SyntaxError as exc:
            return False, f"syntaxe invalide ({exc.msg} l.{exc.lineno})."
        has_run = any(
            isinstance(n, ast.FunctionDef) and n.name == "run"
            and n.args.args and n.args.args[0].arg == "args"
            for n in ast.walk(tree)
        )
        if not has_run:
            return False, "doit définir `def run(args):`."
        return True, ""

    # -- emballage -------------------------------------------------------- #
    def _wrap(self, name: str, description: str, args: dict, code: str) -> str:
        meta = json.dumps({"description": description, "args": args}, ensure_ascii=False)
        harness = (
            "\n\nif __name__ == '__main__':\n"
            "    import sys, json\n"
            "    _a = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}\n"
            "    try:\n"
            "        _out = run(_a)\n"
            "    except Exception as _e:\n"
            "        _out = '[erreur outil: ' + repr(_e) + ']'\n"
            "    print(_out if isinstance(_out, str) else repr(_out))\n"
        )
        return f"{_META_PREFIX}{meta}\n# outil forgé : {name}\n{code.rstrip()}\n{harness}"

    # -- enregistrement --------------------------------------------------- #
    def _register(self, name: str, description: str, args: dict) -> None:
        register_tool(ToolSpec(name=name, description=description, args=args,
                               meta=False, generated=True))

    def is_generated(self, name: str) -> bool:
        spec = get_tool(name)
        return bool(spec and spec.generated)

    def container_path(self, name: str) -> str:
        return f"{self.container_mount}/{name}.py"

    # -- chargement d'une version de stratégie --------------------------- #
    def load_policy_tools(self, policy) -> int:
        """Stage et enregistre les outils portés par `policy` (policy/vN/tools/).

        Renvoie le nombre d'outils chargés. À appeler avant la phase réelle.
        """
        count = 0
        for fname, text in policy.tools.items():
            name = Path(fname).stem
            if name in BUILTIN_NAMES:
                continue
            (self.live_dir / f"{name}.py").write_text(text, encoding="utf-8")
            meta = self._parse_meta(text)
            self._register(name, meta.description, meta.args)
            count += 1
        return count

    def _parse_meta(self, text: str) -> ForgedMeta:
        for line in text.splitlines():
            if line.startswith(_META_PREFIX):
                try:
                    d = json.loads(line[len(_META_PREFIX):])
                    return ForgedMeta(description=d.get("description", ""),
                                      args=d.get("args", {}) or {})
                except json.JSONDecodeError:
                    break
        return ForgedMeta()

    # -- promotion vers une candidate (validée ensuite par la porte ⑩) ---- #
    def promotable_edits(self, tree) -> list[PolicyEdit]:
        """Propose de persister les outils forgés UTILES.

        Un outil est jugé utile s'il a été appelé sur un chemin menant au flag
        (nœud `on_solution_path`). On renvoie une édition `tools/<name>.py` par
        outil, que la boucle RSI ajoute à la candidate avant la validation.
        """
        useful: dict[str, PolicyEdit] = {}
        for attempt in tree.solved_attempts():
            for node in tree.attempt_nodes(attempt.id):
                if not node.on_solution_path or node.action is None:
                    continue
                name = node.action.tool
                if name in useful or not self.is_generated(name):
                    continue
                path = self.live_dir / f"{name}.py"
                if not path.is_file():
                    continue
                useful[name] = PolicyEdit(
                    target=f"tools/{name}.py",
                    rationale=(f"Outil forgé '{name}' utilisé sur un chemin gagnant "
                               f"(challenge {attempt.challenge_name})."),
                    new_content=path.read_text(encoding="utf-8"),
                )
        return list(useful.values())

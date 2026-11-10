"""Définition des tools ③ — les « mains » de l'agent.

Un tool est une fonction nommée que l'agent peut appeler. Le monde (`World`)
exécute l'action ; ce module se contente de **déclarer** les tools et de donner
leur schéma au LLM, plus quelques tools « méta » traités par la boucle d'agent
elle-même (set_hypothesis, submit_flag).

Les tools concrets (run_cmd, python_exec, http…) sont volontairement exécutés
par la sandbox ③ ou le simulateur ⑦, pas ici : cela garde la même interface en
réel et en rêve.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ToolSpec:
    name: str
    description: str
    # Schéma d'arguments simplifié : nom -> description.
    args: dict[str, str]
    # True si la boucle d'agent le traite elle-même (sans passer par le monde).
    meta: bool = False
    # True si l'outil a été FORGÉ par l'agent (option 2). Son code est exécuté
    # dans la sandbox, jamais sur l'hôte.
    generated: bool = False


# Jeu de tools générique, partagé par toutes les catégories. Les agents
# spécialisés pourront en ajouter via `register_tool`.
_TOOLS: dict[str, ToolSpec] = {}


# Noms réservés : un outil forgé ne peut pas écraser un tool de base.
BUILTIN_NAMES: frozenset[str] = frozenset()  # rempli en bas du module


def register_tool(spec: ToolSpec) -> None:
    _TOOLS[spec.name] = spec


def unregister_generated() -> None:
    """Retire tous les outils forgés du registre (avant de charger une version)."""
    for name in [n for n, s in _TOOLS.items() if s.generated]:
        _TOOLS.pop(name, None)


def all_tools() -> list[ToolSpec]:
    return list(_TOOLS.values())


def get_tool(name: str) -> ToolSpec | None:
    return _TOOLS.get(name)


def tools_prompt() -> str:
    """Description des tools à injecter dans le prompt de l'agent."""
    lines = ["Tu disposes des tools suivants (réponds par UN appel à la fois) :"]
    for t in _TOOLS.values():
        args = ", ".join(f"{k}: {v}" for k, v in t.args.items()) or "aucun"
        tag = " [forgé]" if t.generated else ""
        lines.append(f"- `{t.name}`({args}){tag} — {t.description}")
    lines.append(
        "\nFormat de réponse OBLIGATOIRE (JSON strict, rien d'autre) :\n"
        '{"hypothesis": "<ton hypothèse courante>", '
        '"tool": "<nom>", "args": {<arguments>}}'
    )
    return "\n".join(lines)


# -- tools par défaut -------------------------------------------------------- #
register_tool(ToolSpec(
    "run_cmd",
    "Exécute une commande shell dans la sandbox isolée (sans Internet). "
    "Sortie tronquée.",
    {"cmd": "la ligne de commande à exécuter"},
))
register_tool(ToolSpec(
    "python_exec",
    "Exécute un court script Python dans la sandbox et renvoie sa sortie.",
    {"code": "le code Python"},
))
register_tool(ToolSpec(
    "read_file",
    "Lit un fichier du workspace du challenge.",
    {"path": "chemin relatif au workspace"},
))
register_tool(ToolSpec(
    "remote",
    "Envoie des données à un service distant (nc/http) et renvoie la réponse.",
    {"data": "octets/texte à envoyer", "expect": "(optionnel) motif attendu"},
))
register_tool(ToolSpec(
    "set_hypothesis",
    "Ouvre une nouvelle branche de recherche avec une hypothèse explicite.",
    {"text": "l'hypothèse à explorer"},
    meta=True,
))
register_tool(ToolSpec(
    "submit_flag",
    "Soumet un flag candidat. Clôt la tentative si le format est valide.",
    {"flag": "le flag, p. ex. csaw{...}"},
    meta=True,
))
register_tool(ToolSpec(
    "create_tool",
    "Quand tu es BLOQUÉ : forge un nouvel outil réutilisable. Fournis un corps "
    "de fonction `run(args: dict) -> str` en Python. Il sera exécuté dans la "
    "sandbox (sans Internet) et disponible pour la suite. À réserver aux "
    "besoins récurrents (décodeur, solveur, parseur) qu'aucun tool existant ne "
    "couvre.",
    {
        "name": "nom de l'outil (identifiant, sans écraser un tool existant)",
        "description": "ce que fait l'outil",
        "args": "schéma des arguments, dict nom->description",
        "code": "corps Python définissant `def run(args: dict) -> str:`",
    },
    meta=True,
))

# Noms que l'agent ne peut pas écraser en forgeant un outil.
BUILTIN_NAMES = frozenset(_TOOLS.keys())

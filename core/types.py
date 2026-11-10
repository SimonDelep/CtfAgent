"""Types partagés de CtfAgent (architecture Dream-RSI du README).

Ces structures circulent entre le chargeur ①, la boucle d'agent ⑤, l'arbre ⑥,
la phase de rêve ⑦⑧⑨ et la porte de validation ⑩. Elles sont sans dépendance
lourde pour rester importables et testables hors ligne.

Rappel du principe : **les poids du modèle ne changent jamais**. Ce qui évolue,
c'est la *stratégie* (`policy/vN/`, des fichiers texte). L'arbre de recherche
garde la mémoire des tentatives ; le rêve rejoue les mauvaises bifurcations ;
le réflecteur en tire des modifications de stratégie ; la porte n'adopte une
nouvelle stratégie que si elle fait réellement mieux.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

# Catégories de la base CSAW26_LLMAC_DB (indicatif ; l'agent est unique).
CATEGORIES: tuple[str, ...] = ("web", "crypto", "rev", "pwn", "forensics", "misc")

# Format de flag par défaut des Quals CSAW ; configurable par challenge.
DEFAULT_FLAG_REGEX = r"[Cc][Ss][Aa][Ww]\{[^}]{1,200}\}"


# --------------------------------------------------------------------------- #
# Challenge (sortie du chargeur ①)
# --------------------------------------------------------------------------- #
@dataclass
class Challenge:
    """Un challenge chargé, tel que l'agent le voit.

    Ni le flag attendu ni les dossiers `solution/` n'y figurent : le chargeur
    les écarte. Le flag attendu reste connu du seul `runner/evaluate.py`.
    """

    name: str
    description: str
    declared_category: str | None = None
    files: list[str] = field(default_factory=list)  # relatifs au workspace
    host: str | None = None
    port: int | None = None
    workspace: Path | None = None
    flag_regex: str = DEFAULT_FLAG_REGEX
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def has_service(self) -> bool:
        return bool(self.host and self.port)


# --------------------------------------------------------------------------- #
# Actions et observations (boucle d'agent ⑤ / monde ③⑦)
# --------------------------------------------------------------------------- #
@dataclass
class Action:
    """Une décision de l'agent : appeler un tool avec des arguments."""

    tool: str
    args: dict[str, Any] = field(default_factory=dict)
    # Hypothèse courante ; `set_hypothesis` ouvre une nouvelle branche de l'arbre.
    hypothesis: str | None = None

    def key(self) -> str:
        """Clé canonique pour retrouver une action identique dans l'arbre."""
        import json

        return self.tool + "::" + json.dumps(self.args, sort_keys=True, ensure_ascii=False)


@dataclass
class Observation:
    """Résultat d'une action, renvoyé par le monde (sandbox ou simulateur)."""

    output: str
    exit_code: int | None = None
    truncated: bool = False
    simulated: bool = False  # True si produit par le simulateur ⑦
    # True si l'action inconnue n'a pas pu être simulée ([NON SIMULÉ]).
    unsimulated: bool = False


@runtime_checkable
class World(Protocol):
    """Monde dans lequel l'agent agit. Même interface en réel et en rêve.

    - Réel : `core.sandbox.Sandbox` exécute dans Docker ③.
    - Rêve : `dream.simulator.Simulator` rejoue l'arbre ⑦.
    """

    def step(self, action: Action) -> Observation: ...

    def reset(self) -> None: ...


# --------------------------------------------------------------------------- #
# Arbre de recherche ⑥
# --------------------------------------------------------------------------- #
@dataclass
class Node:
    """Un nœud de l'arbre : l'état atteint après une action."""

    id: int
    parent_id: int | None
    attempt_id: str
    action: Action | None  # None pour la racine
    observation: Observation | None
    depth: int = 0
    hypothesis: str | None = None
    # Marqué True si ce nœud est sur le chemin qui a mené au flag.
    on_solution_path: bool = False
    ts: float = field(default_factory=time.time)


@dataclass
class Attempt:
    """Une tentative complète de l'agent sur un challenge."""

    id: str
    challenge_name: str
    policy_version: str
    solved: bool = False
    flag: str | None = None
    steps: int = 0
    root_id: int | None = None
    solution_leaf_id: int | None = None


# --------------------------------------------------------------------------- #
# Stratégie ④ (ce qui apprend)
# --------------------------------------------------------------------------- #
@dataclass
class ForgedTool:
    """Un outil fabriqué par l'agent (option 2). Son code est écrit par le LLM
    et n'est JAMAIS exécuté sur l'hôte : seulement dans la sandbox ③."""

    name: str
    description: str
    args: dict[str, str] = field(default_factory=dict)  # nom -> description
    code: str = ""  # contenu complet du fichier .py (en-tête méta + run() + harnais)


@dataclass
class Policy:
    """Une version de stratégie, chargée depuis `policy/vN/`."""

    version: str  # "v0", "v1", …
    path: Path
    prompt: str = ""
    heuristics: str = ""
    skills: dict[str, str] = field(default_factory=dict)  # nom -> contenu md
    # Outils forgés portés par cette version (nom -> contenu du fichier .py).
    tools: dict[str, str] = field(default_factory=dict)

    def system_prompt(self, extra: str = "") -> str:
        """Assemble le prompt système à partir du prompt et des heuristiques."""
        parts = [self.prompt.strip()]
        if self.heuristics.strip():
            parts.append("## Heuristiques de recherche\n\n" + self.heuristics.strip())
        if extra.strip():
            parts.append(extra.strip())
        return "\n\n".join(p for p in parts if p)


# --------------------------------------------------------------------------- #
# Rêve ⑦⑧⑨
# --------------------------------------------------------------------------- #
@dataclass
class Dream:
    """Un rêve : relance de l'agent depuis une mauvaise bifurcation."""

    branch_node_id: int
    challenge_name: str
    # Note du juge ⑧ : la branche a-t-elle rejoint le chemin gagnant, en combien
    # d'étapes ? Un flag *rêvé* ne compte jamais comme une vraie résolution.
    rejoined_solution_path: bool = False
    steps_to_rejoin: int | None = None
    score: float = 0.0
    transcript: list[tuple[Action, Observation]] = field(default_factory=list)
    lesson: str = ""  # ce que le rêve suggère d'apprendre


@dataclass
class PolicyEdit:
    """Une modification de stratégie proposée par le réflecteur ⑨."""

    target: str  # "prompt", "heuristics", ou "skills/<nom>.md"
    rationale: str
    new_content: str  # contenu complet du fichier cible après édition


@dataclass
class Candidate:
    """Stratégie candidate v(n+1) issue de la réflexion."""

    from_version: str
    version: str
    edits: list[PolicyEdit] = field(default_factory=list)


# --------------------------------------------------------------------------- #
# Validation ⑩ et rapport final
# --------------------------------------------------------------------------- #
@dataclass
class GateResult:
    """Verdict de la porte : adopter la candidate ou la rejeter."""

    adopted: bool
    baseline_solved: int
    candidate_solved: int
    baseline_steps: int
    candidate_steps: int
    reason: str = ""


@dataclass
class EvalResult:
    """Résultat d'une évaluation sur un ensemble de challenges."""

    policy_version: str
    total: int
    solved: int
    total_steps: int
    per_challenge: dict[str, bool] = field(default_factory=dict)

    @property
    def score(self) -> tuple[int, int]:
        """Ordre lexicographique : plus de flags, puis moins d'étapes."""
        return (self.solved, -self.total_steps)


@dataclass
class RSIReport:
    """Trace de toute la boucle RSI, de v0 à l'évaluation finale."""

    iterations: int = 0
    adopted_versions: list[str] = field(default_factory=list)
    gate_history: list[GateResult] = field(default_factory=list)
    final_eval: EvalResult | None = None
    notes: list[str] = field(default_factory=list)

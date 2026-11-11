"""
Mise en texte d'une tentative pour le LLM (réflexion sur les échecs, leçons).
Turns an attempt from the search tree into a compact text the LLM can read.
"""
from __future__ import annotations

import json

from core.tree import SearchTree
from core.types import Action, Observation


def attempt_trace(tree: SearchTree, attempt_id: str, *, max_obs: int = 400,
                  max_chars: int = 8000) -> str:
    """Résume une tentative étape par étape (hypothèse, action, sortie tronquée).
    Branches are kept: each line shows its depth so the model sees the forks.
    """
    lines: list[str] = []
    for node in tree.attempt_nodes(attempt_id):
        if node.action is None:
            continue  # root
        indent = "  " * max(node.depth - 1, 0)
        lines.append(f"{indent}- [{node.depth}] {_fmt(node.action)}")
        if node.observation is not None:
            lines.append(f"{indent}  → {_short(node.observation.output, max_obs)}")
    text = "\n".join(lines)
    # Keep the END of the trace when too long: that is where the model got stuck
    if len(text) > max_chars:
        text = "[…début tronqué…]\n" + text[-max_chars:]
    return text or "(aucune action)"


def transcript_text(transcript: list[tuple[Action, Observation]], *, max_obs: int = 300) -> str:
    """Met en texte le transcript d'un rêve."""
    return "\n".join(f"- {_fmt(a)}\n  → {_short(o.output, max_obs)}" for a, o in transcript) \
        or "(aucune action)"


# Action on one line
def _fmt(action: Action) -> str:
    return f"{action.tool} {json.dumps(action.args, ensure_ascii=False)}"


# Output on one line, truncated
def _short(text: str | None, n: int) -> str:
    flat = (text or "").replace("\n", " ⏎ ")
    return flat if len(flat) <= n else flat[:n] + " […]"

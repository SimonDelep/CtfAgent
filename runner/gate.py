"""Porte de validation ⑩ — adopte une stratégie candidate seulement si meilleure.

Compare les résultats d'évaluation de la stratégie en place (baseline) et de la
candidate sur le MÊME ensemble de validation. Règle d'adoption :

    la candidate est adoptée si elle résout **au moins autant** de challenges,
    et, à nombre égal de flags, en **strictement moins** d'étapes.

Ainsi une candidate ne peut jamais faire régresser le nombre de flags.
"""
from __future__ import annotations

from core.types import EvalResult, GateResult


def decide(baseline: EvalResult, candidate: EvalResult) -> GateResult:
    """Renvoie le verdict d'adoption de la candidate."""
    better_solved = candidate.solved > baseline.solved
    same_solved = candidate.solved == baseline.solved
    fewer_steps = candidate.total_steps < baseline.total_steps

    adopted = better_solved or (same_solved and fewer_steps)

    if better_solved:
        reason = (f"Candidate adoptée : +{candidate.solved - baseline.solved} flag(s) "
                  f"({baseline.solved} → {candidate.solved}).")
    elif same_solved and fewer_steps:
        reason = (f"Candidate adoptée : même nombre de flags ({candidate.solved}), "
                  f"mais {baseline.total_steps - candidate.total_steps} étape(s) de moins.")
    elif same_solved:
        reason = (f"Candidate rejetée : autant de flags ({candidate.solved}) sans gain "
                  f"d'étapes ({candidate.total_steps} ≥ {baseline.total_steps}).")
    else:
        reason = (f"Candidate rejetée : moins de flags "
                  f"({candidate.solved} < {baseline.solved}).")

    return GateResult(
        adopted=adopted,
        baseline_solved=baseline.solved,
        candidate_solved=candidate.solved,
        baseline_steps=baseline.total_steps,
        candidate_steps=candidate.total_steps,
        reason=reason,
    )

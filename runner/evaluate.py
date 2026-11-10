"""Évaluation ⑩/finale — exécute l'agent sur un ensemble et compare au vrai flag.

C'est le **seul** composant autorisé à lire le flag attendu (dans
`challenge.json`). L'agent, lui, ne le voit jamais. L'évaluation renvoie un
`EvalResult` : nombre de flags trouvés et total d'étapes, pour comparer deux
stratégies.
"""
from __future__ import annotations

import json
from pathlib import Path

from core.agent import Agent
from core.loader import load_challenge
from core.sandbox import Sandbox
from core.tree import SearchTree
from core.types import EvalResult, Policy


def _expected_flag(challenge_dir: str | Path) -> str | None:
    """Lit le flag attendu directement depuis challenge.json (jamais exposé à l'agent)."""
    manifest = Path(challenge_dir) / "challenge.json"
    try:
        meta = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    for key in ("flag", "flags", "answer"):
        if key in meta and meta[key]:
            val = meta[key]
            return val[0] if isinstance(val, list) and val else str(val)
    return None


def evaluate(
    policy: Policy,
    challenge_dirs: list[str | Path],
    *,
    llm,
    tree: SearchTree,
    workspace_root: str | Path,
    enable_sandbox: bool = False,
    max_steps: int = 25,
    forge=None,
) -> EvalResult:
    """Évalue une stratégie sur une liste de challenges.

    Args:
        enable_sandbox: n'activer que pour une vraie exécution Docker.
        forge: forgeron d'outils (option 2) pour exécuter les outils forgés que
            la stratégie porte. None => outils forgés indisponibles.
    """
    workspace_root = Path(workspace_root)
    agent = Agent(llm, tree, max_steps=max_steps, forge=forge)
    per: dict[str, bool] = {}
    total_steps = 0
    solved = 0

    for cdir in challenge_dirs:
        cdir = Path(cdir)
        ws = workspace_root / cdir.name
        challenge = load_challenge(cdir, workspace=ws)
        sandbox = Sandbox(ws, enabled=enable_sandbox, forge=forge)
        attempt = agent.run(challenge, policy, sandbox)

        expected = _expected_flag(cdir)
        ok = bool(attempt.solved and expected and attempt.flag == expected)
        # Repli : si pas de flag attendu renseigné, on se fie au format validé.
        if attempt.solved and expected is None:
            ok = True
        per[challenge.name] = ok
        solved += int(ok)
        total_steps += attempt.steps or max_steps

    return EvalResult(
        policy_version=policy.version,
        total=len(challenge_dirs),
        solved=solved,
        total_steps=total_steps,
        per_challenge=per,
    )

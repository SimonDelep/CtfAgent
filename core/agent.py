"""Boucle d'agent ⑤ — le cœur commun au réel et au rêve.

Le LLM choisit un tool, on l'exécute dans le `World` (sandbox ③ en réel,
simulateur ⑦ en rêve), on lui renvoie l'observation, et on recommence. Chaque
étape est enregistrée dans l'arbre ⑥. La seule différence réel/rêve est le
`World` injecté : **le même code tourne dans les deux phases**.

L'agent s'arrête quand il soumet un flag au bon format, ou au bout de
`max_steps`.
"""
from __future__ import annotations

import json
import re
import uuid

from core.llm import LLMClient, LLMError
from core.tools import get_tool, tools_prompt
from core.tree import SearchTree
from core.types import Action, Attempt, Challenge, Observation, Policy, World


class Agent:
    """Agent unique piloté par une stratégie `Policy`."""

    def __init__(self, llm: LLMClient | None, tree: SearchTree, *, max_steps: int = 25,
                 forge=None) -> None:
        self.llm = llm
        self.tree = tree
        self.max_steps = max_steps
        # Forgeron d'outils (option 2) ; None => create_tool indisponible.
        self.forge = forge

    def run(self, challenge: Challenge, policy: Policy, world: World) -> Attempt:
        """Attaque un challenge et renvoie la tentative (arbre enregistré)."""
        attempt = Attempt(
            id=uuid.uuid4().hex[:12],
            challenge_name=challenge.name,
            policy_version=policy.version,
        )
        root_id = self.tree.start_attempt(attempt)
        world.reset()

        messages = [
            {"role": "system", "content": policy.system_prompt(tools_prompt())},
            {"role": "user", "content": _challenge_brief(challenge)},
        ]

        current_parent = root_id
        hypothesis: str | None = None

        for step in range(1, self.max_steps + 1):
            action = self._decide(messages)
            if action is None:
                break

            # Tools « méta » traités par la boucle elle-même.
            if action.tool == "set_hypothesis":
                hypothesis = action.args.get("text", "") or action.hypothesis
                obs = Observation(output=f"[hypothèse: {hypothesis}]")
                node_id = self.tree.add_node(attempt.id, current_parent, action, obs,
                                             hypothesis=hypothesis)
                current_parent = node_id  # nouvelle branche
                messages.append({"role": "assistant", "content": _fmt_action(action)})
                messages.append({"role": "user", "content": obs.output})
                continue

            if action.tool == "create_tool":
                obs = self._handle_create_tool(action)
                node_id = self.tree.add_node(attempt.id, current_parent, action, obs,
                                             hypothesis=hypothesis)
                current_parent = node_id
                messages.append({"role": "assistant", "content": _fmt_action(action)})
                messages.append({"role": "user", "content": obs.output})
                continue

            if action.tool == "submit_flag":
                flag = (action.args.get("flag", "") or "").strip()
                obs = Observation(output=f"[flag soumis: {flag}]")
                node_id = self.tree.add_node(attempt.id, current_parent, action, obs,
                                             hypothesis=hypothesis)
                if re.search(challenge.flag_regex, flag):
                    attempt.solved = True
                    attempt.flag = flag
                    attempt.steps = step
                    self.tree.mark_solution_path(attempt.id, node_id, flag, step)
                    return attempt
                messages.append({"role": "assistant", "content": _fmt_action(action)})
                messages.append({"role": "user",
                                 "content": "Flag au mauvais format, continue."})
                current_parent = node_id
                continue

            # Tool concret : exécuté par le monde.
            if get_tool(action.tool) is None:
                obs = Observation(output=f"[tool inconnu: {action.tool}]")
            else:
                obs = world.step(action)

            node_id = self.tree.add_node(attempt.id, current_parent, action, obs,
                                         hypothesis=hypothesis)
            current_parent = node_id
            attempt.steps = step

            # Un flag peut apparaître dans la sortie sans soumission explicite.
            found = re.search(challenge.flag_regex, obs.output or "")
            if found:
                flag = found.group(0)
                attempt.solved = True
                attempt.flag = flag
                self.tree.mark_solution_path(attempt.id, node_id, flag, step)
                return attempt

            messages.append({"role": "assistant", "content": _fmt_action(action)})
            messages.append({"role": "user", "content": _observation_text(obs)})

        return attempt

    # -- forge (option 2) ------------------------------------------------- #
    def _handle_create_tool(self, action: Action) -> Observation:
        if self.forge is None:
            return Observation(output="[create_tool indisponible : aucun forgeron]")
        res = self.forge.forge(
            name=action.args.get("name", ""),
            description=action.args.get("description", ""),
            args=action.args.get("args", {}),
            code=action.args.get("code", ""),
        )
        if res.ok:
            return Observation(output=(
                f"[outil '{res.name}' créé et disponible ; appelle-le comme un "
                f"tool normal pour l'utiliser]"
            ))
        return Observation(output=f"[create_tool refusé : {res.message}]")

    # -- décision LLM ----------------------------------------------------- #
    def _decide(self, messages: list[dict[str, str]]) -> Action | None:
        if self.llm is None:
            return None  # pas de modèle → l'agent ne peut pas décider
        try:
            raw = self.llm.chat(messages, max_tokens=512)
        except LLMError:
            return None
        return _parse_action(raw)


def _parse_action(raw: str) -> Action | None:
    """Extrait un appel d'action du texte du LLM (JSON toléré, même entouré)."""
    obj = _first_json(raw)
    if obj is None or "tool" not in obj:
        return None
    return Action(
        tool=str(obj.get("tool", "")).strip(),
        args=obj.get("args", {}) if isinstance(obj.get("args"), dict) else {},
        hypothesis=obj.get("hypothesis"),
    )


def _first_json(text: str) -> dict | None:
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    cands = [fence.group(1)] if fence else []
    start = text.find("{")
    while start != -1 and len(cands) < 6:
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    cands.append(text[start:i + 1])
                    break
        start = text.find("{", start + 1)
    for c in cands:
        try:
            o = json.loads(c)
            if isinstance(o, dict):
                return o
        except json.JSONDecodeError:
            continue
    return None


def _fmt_action(action: Action) -> str:
    return json.dumps({"hypothesis": action.hypothesis, "tool": action.tool,
                       "args": action.args}, ensure_ascii=False)


def _observation_text(obs: Observation) -> str:
    if obs.unsimulated:
        return "[NON SIMULÉ]"
    prefix = "[simulé] " if obs.simulated else ""
    return prefix + (obs.output or "")


def _challenge_brief(challenge: Challenge) -> str:
    parts = [f"# Challenge : {challenge.name}", "", challenge.description.strip()]
    if challenge.files:
        parts.append("\nFichiers disponibles : " + ", ".join(challenge.files))
    if challenge.has_service:
        parts.append(f"Service distant : {challenge.host}:{challenge.port}")
    parts.append("\nTrouve le flag et soumets-le avec le tool submit_flag.")
    return "\n".join(parts)

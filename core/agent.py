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
from core.trace import get_tracer
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

        # Announce the challenge (everything after goes into its own log file)
        t = get_tracer()
        t.start_challenge(challenge.name, attempt=attempt.id, policy=policy.version,
                          category=challenge.declared_category, files=challenge.files,
                          service=f"{challenge.host}:{challenge.port}" if challenge.has_service else None)
        # Actions already tried, to detect when the model goes round in circles
        seen: set[str] = set()

        messages = [
            {"role": "system", "content": policy.system_prompt(tools_prompt())},
            {"role": "user", "content": _challenge_brief(challenge)},
        ]

        current_parent = root_id
        hypothesis: str | None = None

        for step in range(1, self.max_steps + 1):
            action = self._decide(messages)
            if action is None:
                t.event("block", f"Aucune action exploitable à l'étape {step} : arrêt")
                break

            # What the model tries to do
            t.event("action", f"#{step} {action.tool} {json.dumps(action.args, ensure_ascii=False)}")
            if action.key() in seen:
                t.event("block", "Action déjà tentée : le modèle tourne en rond")
            seen.add(action.key())

            # Tools « méta » traités par la boucle elle-même.
            if action.tool == "set_hypothesis":
                hypothesis = action.args.get("text", "") or action.hypothesis
                obs = Observation(output=f"[hypothèse: {hypothesis}]")
                _trace_obs(obs)
                node_id = self.tree.add_node(attempt.id, current_parent, action, obs,
                                             hypothesis=hypothesis)
                current_parent = node_id  # nouvelle branche
                messages.append({"role": "assistant", "content": _fmt_action(action)})
                messages.append({"role": "user", "content": obs.output})
                continue

            if action.tool == "create_tool":
                obs = self._handle_create_tool(action)
                _trace_obs(obs)
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
                    t.event("flag", f"✔ Flag soumis : {flag} ({step} étapes)")
                    t.end_challenge()
                    return attempt
                t.event("block", f"Flag rejeté (mauvais format) : {flag}")
                messages.append({"role": "assistant", "content": _fmt_action(action)})
                messages.append({"role": "user",
                                 "content": "Flag au mauvais format, continue."})
                current_parent = node_id
                continue

            # Tool concret : exécuté par le monde.
            if get_tool(action.tool) is None:
                obs = Observation(output=f"[tool inconnu: {action.tool}]")
            else:
                # A crash of the world (Docker, sandbox…) must still appear in the logs
                try:
                    obs = world.step(action)
                except Exception as exc:
                    t.event("block", f"Exception pendant l'action : {exc!r}")
                    t.end_challenge()
                    raise
            _trace_obs(obs)

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
                t.event("flag", f"✔ Flag trouvé dans la sortie : {flag} ({step} étapes)")
                t.end_challenge()
                return attempt

            messages.append({"role": "assistant", "content": _fmt_action(action)})
            messages.append({"role": "user", "content": _observation_text(obs)})

        # Out of steps (or model stopped answering)
        t.event("block", f"✘ Échec : pas de flag après {attempt.steps} étape(s) "
                         f"(max={self.max_steps})")
        t.end_challenge()
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
        t = get_tracer()
        # Bigger budget: the thinking phase consumes tokens before the JSON answer
        try:
            raw, reasoning = self.llm.chat_full(messages, max_tokens=4096)
        except LLMError as exc:
            t.event("block", f"Erreur LLM : {exc}")
            return None
        # What the model thinks
        if reasoning:
            t.event("think", reasoning)
        action = _parse_action(raw)
        if action is None:
            t.event("block", "Réponse sans JSON d'action exploitable", raw=raw)
            return None
        # Text written around the JSON is also part of its reasoning
        prose = _strip_json(raw)
        if prose:
            t.event("think", prose)
        if action.hypothesis:
            t.event("think", f"Hypothèse : {action.hypothesis}")
        return action


def _trace_obs(obs: Observation) -> None:
    """Affiche le résultat d'une action et signale les blocages.
    Shows an action result and flags blocking situations.
    """
    t = get_tracer()
    out = obs.output or ""
    t.event("result", out or "(sortie vide)", exit_code=obs.exit_code,
            truncated=obs.truncated, simulated=obs.simulated)
    # Known failure signals coming from the sandbox / simulator / forge
    failed = (
        obs.unsimulated
        or (obs.exit_code not in (None, 0))
        or out.startswith(("[tool inconnu", "[create_tool", "[timeout", "[accès refusé",
                           "[fichier introuvable", "[lecture impossible", "[remote non"))
    )
    if failed:
        t.event("block", f"Échec de l'action (exit={obs.exit_code}) : {out[:200]}")


def _strip_json(raw: str) -> str:
    """Retire le bloc JSON d'action et renvoie le texte libre restant."""
    text = re.sub(r"```(?:json)?\s*\{.*?\}\s*```", "", raw, flags=re.DOTALL)
    obj_start = text.find("{")
    obj_end = text.rfind("}")
    if obj_start != -1 and obj_end > obj_start:
        text = text[:obj_start] + text[obj_end + 1:]
    return text.strip()


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

"""Boucle ReAct : think -> act -> observe, avec :
  - détecteur de BLOCAGE (nudge → forge un outil) ;
  - détecteur de RÉPÉTITION (appel identique court-circuité + avertissement) ;
  - RÉSUMÉ périodique (tous les N tours) écrit dans summary.md + compactage du contexte
    (mémoire d'approches : le résumé remplace l'historique détaillé) ;
  - AFFICHAGE live (pensée / action / résultat) dans le terminal.
Un flag n'est accepté que 'grounded' (présent dans une sortie d'outil réelle).
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from datetime import datetime

from .console import Console
from .context import RunContext
from .registry import ToolRegistry
from .report import Transcript
from .verifier import FlagVerifier

_META = {"forge_tool", "edit_tool", "list_tools", "submit_flag"}


@dataclass
class RunResult:
    flag: str | None
    solved: bool
    correct: bool | None
    steps: int
    tokens: int
    seconds: float
    forged_tools: int
    reason: str


class AgentLoop:
    def __init__(self, llm, ctx: RunContext, transcript: Transcript, budget: dict, options: dict | None = None):
        opts = options or {}
        self.llm = llm
        self.ctx = ctx
        self.reg: ToolRegistry = ctx.registry
        self.verifier: FlagVerifier = ctx.verifier
        self.transcript = transcript
        self.max_steps = int(budget.get("max_steps", 40))
        self.max_tokens = int(budget.get("max_tokens_total", 400000))
        self.wall = int(budget.get("wall_clock_seconds", 2400))
        self.stuck_threshold = int(opts.get("stuck_threshold", 3))
        self.repeat_threshold = int(opts.get("repeat_threshold", 3))
        self.summary_interval = int(opts.get("summary_interval", 10))
        self.console = Console(bool(opts.get("stream", True)))
        self.summary_path = transcript.run_dir / "summary.md"

        self._no_progress = 0
        self._call_counts: dict[str, int] = {}
        self._call_cache: dict[str, dict] = {}
        self._last_summary_idx = 0
        self._running_summary = ""   # résumé CUMULATIF (intègre tout l'historique, borné)

    def run(self, system_prompt: str, user_prompt: str) -> RunResult:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        self.transcript.log("system", content=system_prompt)
        self.transcript.log("user", content=user_prompt)
        self.console.info(f"Challenge lancé — budget {self.max_steps} tours. Modèle : {self.llm.model}")

        t0 = time.time()

        for step in range(1, self.max_steps + 1):
            if time.time() - t0 > self.wall:
                return self._finish(None, step, t0, "budget: wall-clock dépassé")
            if self.llm.total_usage.total_tokens > self.max_tokens:
                return self._finish(None, step, t0, "budget: tokens dépassés")

            self.console.step(step, self.max_steps)
            resp = self.llm.chat(messages, tools=self.reg.schemas())
            self.console.think(resp.thought or "")
            self.transcript.log("assistant", content=resp.content, thought=resp.thought,
                                tool_calls=[tc["name"] for tc in resp.tool_calls],
                                tokens=resp.usage.total_tokens)

            assistant_msg = {"role": "assistant", "content": resp.content or ""}
            if resp.tool_calls:
                assistant_msg["tool_calls"] = [{
                    "id": tc["id"] or f"call_{step}_{i}", "type": "function",
                    "function": {"name": tc["name"], "arguments": json.dumps(tc["arguments"])},
                } for i, tc in enumerate(resp.tool_calls)]
            messages.append(assistant_msg)

            if not resp.tool_calls:
                self._no_progress += 1
                self.console.warn("aucun outil appelé — relance.")
                messages.append({"role": "user", "content": self._nudge()})
                self._maybe_summarize(step, messages)
                continue

            progressed = False
            for i, tc in enumerate(resp.tool_calls):
                name, args = tc["name"], tc["arguments"]
                call_id = tc["id"] or f"call_{step}_{i}"
                self.console.action(name, args)
                self.transcript.log("tool_call", name=name, arguments=args)

                result, repeated = self._dispatch_with_repeat_guard(name, args)
                self.console.result(name, result)
                self.transcript.log("tool_result", name=name, result=result, repeated=repeated)

                for key in ("stdout", "stderr"):
                    if isinstance(result, dict) and result.get(key):
                        self.verifier.observe(result[key])
                if not repeated and _is_progress(name, result):
                    progressed = True

                messages.append(_tool_msg(call_id, name, result))

                if name == "submit_flag" and self.ctx.accepted_flag:
                    self.console.success(f"FLAG accepté : {self.ctx.accepted_flag}")
                    return self._finish(self.ctx.accepted_flag, step, t0, "flag accepté (grounded)")

                cands = self.verifier.candidates_from_observations()
                hit = next((c for c in cands if self.verifier.validate(c)["accepted"]), None)
                if hit:
                    self.console.success(f"FLAG détecté dans une sortie d'outil : {hit}")
                    self.transcript.log("auto_flag", flag=hit)
                    return self._finish(hit, step, t0, "flag détecté dans une sortie d'outil")

            self._no_progress = 0 if progressed else self._no_progress + 1
            if self._no_progress >= self.stuck_threshold:
                self.console.warn(f"bloqué depuis {self._no_progress} tours — nudge Forge.")
                messages.append({"role": "user", "content": self._nudge()})
                self._no_progress = 0

            self._maybe_summarize(step, messages)

        return self._finish(None, self.max_steps, t0, "budget: max_steps atteint")

    # --- répétition ------------------------------------------------------
    def _dispatch_with_repeat_guard(self, name: str, args: dict):
        if name in _META:
            return self.reg.dispatch(name, args, self.ctx), False
        sig = _sig(name, args)
        self._call_counts[sig] = self._call_counts.get(sig, 0) + 1
        n = self._call_counts[sig]
        if n >= self.repeat_threshold and sig in self._call_cache:
            self.console.warn(f"appel '{name}' répété {n}× — court-circuité.")
            warn = {
                "repeated_call": True,
                "note": (f"Appel IDENTIQUE déjà exécuté {n}× — résultat inchangé ci-dessous. "
                         "ARRÊTE de le répéter : change d'hypothèse, forge/édite un outil, "
                         "ou soumets le flag s'il est déjà apparu."),
                "previous_result": self._call_cache[sig],
            }
            return warn, True
        result = self.reg.dispatch(name, args, self.ctx)
        if isinstance(result, dict):
            self._call_cache[sig] = result
        return result, False

    # --- résumé + compactage du contexte --------------------------------
    def _maybe_summarize(self, step: int, messages: list[dict]) -> None:
        if self.summary_interval <= 0 or step % self.summary_interval != 0:
            return
        summary = self._summarize(step)
        # compactage : on remplace l'historique détaillé par le résumé (mémoire d'approches)
        messages[:] = [
            messages[0],  # system
            messages[1],  # énoncé original
            {"role": "user", "content":
                "MÉMOIRE DE PROGRESSION (résumé à jour de ce que tu as fait et des échecs — "
                "ne répète pas les approches ratées) :\n\n" + summary +
                "\n\nContinue à partir d'ici."},
        ]
        self.console.info(f"résumé écrit (tour {step}) -> {self.summary_path.name} ; contexte compacté.")

    def _summarize(self, step: int) -> str:
        events = self.transcript.events[self._last_summary_idx:]
        self._last_summary_idx = len(self.transcript.events)
        convo = _render_events(events)
        prev = self._running_summary.strip()
        if len(prev) > 8000:   # garde-fou : le cumul ne doit pas enfler le contexte
            prev = "…(début tronqué)…\n" + prev[-8000:]
        prev_block = (
            "Résumé CUMULATIF précédent (à mettre à jour, PAS à repartir de zéro — "
            "conserve tout ce qui reste pertinent) :\n\n" + prev + "\n\n"
        ) if prev else ""
        prompt = (
            "Mets à jour le résumé CUMULATIF de ta résolution en Markdown, en 4 sections brèves. "
            "Il doit intégrer TOUT l'historique (ancien + nouveau), pas seulement la trajectoire récente :\n"
            "## Fait (actions utiles et ce qu'elles ont donné)\n"
            "## Échecs / impasses (ce qui n'a PAS marché — à ne pas refaire)\n"
            "## État actuel (ce qu'on sait, fichiers/indices clés)\n"
            "## Prochaines pistes\n\n"
            + prev_block +
            "Nouvelle trajectoire depuis le dernier résumé :\n" + convo
        )
        try:
            resp = self.llm.chat(
                [{"role": "system", "content": "Tu résumes honnêtement ta propre progression CTF. "
                  "Tu produis un résumé cumulatif qui remplace le précédent sans rien perdre d'important."},
                 {"role": "user", "content": prompt}],
                temperature=0.3,
            )
            summary = resp.content or _mechanical_summary(self._call_counts)
        except Exception as exc:  # noqa: BLE001
            summary = (prev + "\n" if prev else "") + _mechanical_summary(self._call_counts) + \
                f"\n(résumé LLM indisponible: {exc})"
        self._running_summary = summary   # mémorisé pour le prochain cumul

        header = f"\n\n---\n## Résumé au tour {step} ({datetime.now().strftime('%H:%M:%S')})\n\n"
        with open(self.summary_path, "a", encoding="utf-8") as fh:
            fh.write(header + summary + "\n")
        self.transcript.log("summary", step=step, content=summary)
        return summary

    # --- divers ----------------------------------------------------------
    def _nudge(self) -> str:
        return ("Tu sembles bloqué. (1) FORGE un outil spécialisé (forge_tool) qui encapsule une "
                "approche rejouable (bruteforce, extracteur, client réseau), ou corrige-en un "
                "(edit_tool) ; (2) sinon CHANGE d'hypothèse et collecte une nouvelle observation. "
                "Ne répète pas une commande qui a déjà échoué. Ne devine jamais le flag.")

    def _finish(self, flag, steps, t0, reason) -> RunResult:
        correct = None
        if flag is not None and self.verifier.ground_truth is not None:
            correct = flag == self.verifier.ground_truth
        forged = sum(1 for r in self.reg.describe() if r["kind"] == "forgé")
        res = RunResult(flag=flag, solved=flag is not None, correct=correct, steps=steps,
                        tokens=self.llm.total_usage.total_tokens, seconds=round(time.time() - t0, 1),
                        forged_tools=forged, reason=reason)
        if flag:
            self.console.success(f"Terminé : {flag}  ({reason})")
        else:
            self.console.warn(f"Terminé sans flag : {reason}")
        return res


def _sig(name: str, args: dict) -> str:
    blob = json.dumps(args, sort_keys=True, ensure_ascii=False)
    return name + "|" + hashlib.sha1(blob.encode()).hexdigest()[:12]


def _is_progress(name: str, result) -> bool:
    if name in ("forge_tool", "edit_tool"):
        return bool(isinstance(result, dict) and result.get("ok"))
    if not isinstance(result, dict) or result.get("timed_out"):
        return False
    return result.get("exit_code", 1) == 0 and bool(result.get("stdout"))


def _render_events(events: list[dict]) -> str:
    lines = []
    for e in events:
        r = e.get("role")
        if r == "assistant" and (e.get("thought") or e.get("content")):
            lines.append("[PENSÉE] " + str(e.get("thought") or e.get("content"))[:500])
        elif r == "tool_call":
            lines.append(f"[APPEL {e.get('name')}] " + json.dumps(e.get("arguments", {}), ensure_ascii=False)[:300])
        elif r == "tool_result":
            res = e.get("result", {})
            s = res.get("stdout") or res.get("stderr") or res.get("error") or res.get("message") or "" if isinstance(res, dict) else str(res)
            lines.append("[RÉSULTAT] " + str(s)[:400])
    return "\n".join(lines)[:12000]


def _mechanical_summary(call_counts: dict) -> str:
    top = sorted(call_counts.items(), key=lambda kv: -kv[1])[:10]
    rows = "\n".join(f"- {k.split('|')[0]} ×{v}" for k, v in top)
    return "## Fait\n(résumé mécanique — appels effectués)\n" + rows + "\n## Prochaines pistes\nVarier l'approche."


def _tool_msg(call_id: str, name: str, result) -> dict:
    content = result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)
    return {"role": "tool", "tool_call_id": call_id, "name": name, "content": content}

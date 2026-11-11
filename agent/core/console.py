"""Affichage live de la boucle ReAct dans le terminal : pensée → action → résultat."""
from __future__ import annotations

import json
import os
import sys

_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def _c(code: str, s: str) -> str:
    return f"\033[{code}m{s}\033[0m" if _COLOR else s


def _clip(text: str, n: int = 500) -> str:
    text = (text or "").strip()
    return text if len(text) <= n else text[:n] + " …"


def _first_lines(text: str, n: int = 3, width: int = 300) -> str:
    lines = (text or "").strip().splitlines()
    out = "\n".join("    " + l for l in lines[:n])
    if len(lines) > n:
        out += f"\n    … (+{len(lines)-n} lignes)"
    return _clip(out, width * n)


class Console:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def _p(self, *a):
        if self.enabled:
            print(*a, flush=True)

    def step(self, n: int, maxn: int):
        self._p("\n" + _c("2", f"-------- Tour {n}/{maxn} --------"))

    def think(self, text: str):
        if text and text.strip():
            self._p(_c("36", "pensée : ") + _clip(text, 600))

    def action(self, name: str, args: dict):
        self._p(_c("33", f"[outil] {name}") + _c("2", f"  {self._args_brief(name, args)}"))

    def _args_brief(self, name: str, args: dict) -> str:
        if not isinstance(args, dict):
            return str(args)[:160]
        if name == "run_shell":
            return "$ " + _clip(str(args.get("command", "")), 160)
        if name == "run_python":
            return "code: " + _clip(str(args.get("code", "")).splitlines()[0] if args.get("code") else "", 120)
        if name in ("forge_tool", "edit_tool"):
            return f"name={args.get('name')!r}"
        if name == "submit_flag":
            return f"flag={args.get('flag')!r}"
        return _clip(json.dumps(args, ensure_ascii=False), 160)

    def result(self, name: str, res):
        if not isinstance(res, dict):
            self._p(_c("2", "    -> ") + _clip(str(res), 300))
            return
        if res.get("repeated_call"):
            self._p(_c("31", "    -> [répété] court-circuité"))
            return
        if name in ("forge_tool", "edit_tool"):
            if res.get("ok"):
                self._p(_c("32", "    -> [ok] ") + _clip(res.get("message", ""), 200))
            else:
                self._p(_c("31", "    -> [échec] ") + _clip(res.get("error", ""), 200))
            return
        if name == "submit_flag":
            tag = _c("32", "ACCEPTÉ") if res.get("accepted") else _c("31", "REFUSÉ")
            extra = "" if res.get("accepted") else "  " + _clip(res.get("hint", ""), 160)
            self._p(f"    -> submit_flag : {tag}{extra}")
            return
        if "error" in res and "exit_code" not in res:
            self._p(_c("31", "    -> [échec] ") + _clip(str(res.get("error")), 200))
            return
        code = res.get("exit_code")
        flag = _c("31", "timeout") if res.get("timed_out") else (_c("32", "exit 0") if code == 0 else _c("31", f"exit {code}"))
        self._p(_c("2", "    -> ") + flag)
        if res.get("stdout"):
            self._p(_first_lines(res["stdout"]))
        if res.get("stderr"):
            self._p(_c("31", _first_lines(res["stderr"], 2)))

    def info(self, text: str):
        self._p(_c("35", "[info] " + text))

    def warn(self, text: str):
        self._p(_c("31", "[!] " + text))

    def success(self, text: str):
        self._p(_c("32", "" + text))

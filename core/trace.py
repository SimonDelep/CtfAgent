"""
Affichage console + Journalisation par challenge dans log_dir (data/logs/{run}/)
Console display + Challenge logging into log_dir (data/logs/{run}/)
"""
from __future__ import annotations
import json, os, re, sys, time
from pathlib import Path

_COL = {"think": "2;36", "action": "1;34", "result": "37", "block": "1;31",
        "flag": "1;32", "dream": "35", "reflect": "33", "gate": "1;33",
        "challenge": "1;37", "branch": "1;36", "phase": "1;35", "info": "37"}

class Tracer:

    def __init__(self, log_dir=None, console=True, max_console=400):
        # Activate / Deactivate console output, and define max console length
        self.console, self.max_console = console, max_console
        # If output is console, activate color, else no
        self.color = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
        # Create dir for the log output if doesn't already exist
        self.log_dir = Path(log_dir) if log_dir else None
        if self.log_dir:
            self.log_dir.mkdir(parents=True, exist_ok=True)
        # Store current state of where the model is
        self.phase, self.challenge = "-", None

    # Change state or challenge
    def set_phase(self, phase: str, detail: str = ""):
        self.phase, self.challenge = phase, None
        self.event("phase", f"══ {phase} ══ {detail}")

    def start_challenge(self, name: str, **info):
        self.challenge = name
        self.event("challenge", f"▶ {name}", **info)

    def end_challenge(self):
        self.challenge = None

    # Main
    def event(self, kind: str, msg: str, **data):
        # Console output
        if self.console:
            # Flatten multi-line text so columns stay aligned
            flat = msg.replace("\n", " ⏎ ")
            short = flat if len(flat) <= self.max_console else flat[:self.max_console] + " […]"
            tag = f"[{self.phase}]" + (f"[{self.challenge}]" if self.challenge else "")
            line = f"{tag} {kind.upper():<9} {short}"
            if self.color and kind in _COL:
                line = f"\033[{_COL[kind]}m{line}\033[0m"
            print(line, flush=True)
        # Write in log file jsonl format
        if self.log_dir:
            name = re.sub(r"[^\w.-]+", "_", self.challenge)[:80] if self.challenge else "_run"
            rec = {"ts": time.time(), "phase": self.phase, "challenge": self.challenge,
                   "kind": kind, "msg": msg, **data}
            with open(self.log_dir / f"{name}.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
            with open(self.log_dir / f"{name}.log", "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%H:%M:%S')} [{self.phase}] {kind.upper()}:\n")
                f.write(_indent(msg, "    | ") + "\n")
                for k, v in data.items():
                    v = str(v)
                    # Short values stay on one line, long ones become an indented block
                    if "\n" in v:
                        f.write(f"    {k}:\n" + _indent(v, "      ") + "\n")
                    else:
                        f.write(f"    {k}: {v}\n")

# Indent every line of a text (keeps multi-line blocks readable in .log)
def _indent(text: str, prefix: str) -> str:
    return "\n".join(prefix + l for l in str(text).splitlines() or [""])

# Create Tracer
_TRACER = Tracer(console=False)
def get_tracer() -> Tracer: return _TRACER
def set_tracer(t: Tracer) -> None:
    global _TRACER; _TRACER = t


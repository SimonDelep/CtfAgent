"""Harness de scoring : lance l'agent (autonome) sur un ou tous les challenges, agrège les métriques.

Usage :
    python -m agent.eval.run --only crypto/secret_treaties
    python -m agent.eval.run --pilots
    python -m agent.eval.run            # tous les challenges
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ..config import REPO_ROOT, load_config
from ..core.ledger import Ledger
from ..llm_client import LLMClient
from ..orchestrator import solve_challenge

# Pilotes "faciles" couvrant chaque catégorie (cf. plan).
PILOTS = [
    "crypto/secret_treaties",
    "misc/12345678",
    "forensics/hemispheres",
    "web/flagchecker",
    "rev/autobahn",
]


def discover_all(cfg: dict) -> list[Path]:
    root = REPO_ROOT / cfg["paths"]["challenges_root"]
    return sorted(p.parent for p in root.glob("*/*/challenge.json"))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=None)
    ap.add_argument("--only", help="Un challenge précis, ex: crypto/secret_treaties")
    ap.add_argument("--pilots", action="store_true", help="Les 5 challenges pilotes.")
    ap.add_argument("--force", action="store_true", help="Relance même les challenges déjà résolus.")
    ap.add_argument("--status", action="store_true", help="Affiche le ledger (suivi) et quitte.")
    args = ap.parse_args(argv)

    cfg = load_config(args.config)
    root = REPO_ROOT / cfg["paths"]["challenges_root"]
    ledger = Ledger(REPO_ROOT / cfg["paths"]["runs_dir"] / "ledger.json")

    if args.status:
        print(ledger.summary())
        return 0

    if args.only:
        targets = [root / args.only]
    elif args.pilots:
        targets = [root / p for p in PILOTS]
    else:
        targets = discover_all(cfg)

    llm = LLMClient(cfg)
    if not llm.ping():
        print(f"[!] Endpoint LLM injoignable: {cfg['llm']['base_url']}", file=sys.stderr)
        return 3

    rows = []
    for chal in targets:
        if not (chal / "challenge.json").exists():
            print(f"[skip] {chal} (pas de challenge.json)")
            continue
        name = f"{chal.parent.name}/{chal.name}"
        if not args.force and ledger.is_done(chal.parent.name, chal.name):
            e = ledger.get(chal.parent.name, chal.name)
            print(f"[skip] {name} déjà résolu (flag={e.get('flag')}) — --force pour relancer.")
            rows.append({"challenge": name, **{k: e.get(k) for k in ("solved", "correct", "flag", "steps", "tokens", "reason")}})
            continue
        print(f"[run ] {name} ...", flush=True)
        try:
            res = solve_challenge(chal, cfg, use_ground_truth=True)
            rows.append({"challenge": name, **res.__dict__})
            status = "OK" if res.correct else ("~" if res.solved else "-")
            print(f"[{status:>3}] {name}  flag={res.flag}  steps={res.steps} tok={res.tokens} {res.seconds}s")
        except Exception as exc:  # noqa: BLE001
            rows.append({"challenge": name, "error": str(exc), "solved": False, "correct": False})
            print(f"[ERR] {name}: {exc}")

    _write_report(cfg, rows)
    solved = sum(1 for r in rows if r.get("correct"))
    print(f"\n=== {solved}/{len(rows)} résolus (flag correct) ===")
    return 0


def _write_report(cfg: dict, rows: list[dict]) -> None:
    out = REPO_ROOT / "agent" / "eval" / "report.md"
    lines = ["# Résultats de l'agent CTF\n", "| Challenge | Résolu | Correct | Steps | Tokens | Temps(s) | Raison |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(
            f"| {r.get('challenge')} | {_b(r.get('solved'))} | {_b(r.get('correct'))} | "
            f"{r.get('steps','-')} | {r.get('tokens','-')} | {r.get('seconds','-')} | {r.get('reason', r.get('error',''))} |"
        )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out.parent / "report.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[report] {out}")


def _b(v) -> str:
    return "✅" if v else ("—" if v is None else "❌")


if __name__ == "__main__":
    raise SystemExit(main())

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


def _valid_targets(targets: list[Path]) -> list[Path]:
    out = []
    for chal in targets:
        if (chal / "challenge.json").exists():
            out.append(chal)
        else:
            print(f"[skip] {chal} (pas de challenge.json)")
    return out


def _remaining(targets: list[Path], ledger: Ledger) -> list[Path]:
    """Challenges pas encore résolus correctement (à (re)tenter)."""
    return [c for c in targets if not ledger.is_done(c.parent.name, c.name)]


def _run_pass(targets: list[Path], cfg: dict, ledger: Ledger, force: bool, round_no: int | None) -> dict:
    """Une passe : tente chaque challenge non résolu. Retourne {name: row}."""
    rows: dict[str, dict] = {}
    for chal in targets:
        name = f"{chal.parent.name}/{chal.name}"
        if not force and ledger.is_done(chal.parent.name, chal.name):
            e = ledger.get(chal.parent.name, chal.name) or {}
            print(f"[skip] {name} déjà résolu (flag={e.get('flag')}).")
            rows[name] = {"challenge": name, **{k: e.get(k) for k in ("solved", "correct", "flag", "steps", "tokens", "seconds", "reason")}}
            continue
        tag = f"passe {round_no} · " if round_no else ""
        print(f"[run ] {tag}{name} ...", flush=True)
        try:
            res = solve_challenge(chal, cfg, use_ground_truth=True)
            rows[name] = {"challenge": name, **res.__dict__}
            status = "OK" if res.correct else ("~" if res.solved else "-")
            print(f"[{status:>3}] {name}  flag={res.flag}  steps={res.steps} tok={res.tokens} {res.seconds}s")
        except Exception as exc:  # noqa: BLE001
            rows[name] = {"challenge": name, "error": str(exc), "solved": False, "correct": False}
            print(f"[ERR] {name}: {exc}")
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=None)
    ap.add_argument("--only", help="Un challenge précis, ex: crypto/secret_treaties")
    ap.add_argument("--pilots", action="store_true", help="Les 5 challenges pilotes.")
    ap.add_argument("--force", action="store_true", help="Relance même les challenges déjà résolus (1re passe).")
    ap.add_argument("--once", action="store_true", help="Une seule passe (sinon : relance en boucle jusqu'à tout résoudre).")
    ap.add_argument("--max-rounds", type=int, default=0, help="Nb max de passes (0 = illimité, Ctrl-C pour arrêter).")
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
    targets = _valid_targets(targets)

    llm = LLMClient(cfg)
    if not llm.ping():
        print(f"[!] Endpoint LLM injoignable: {cfg['llm']['base_url']}", file=sys.stderr)
        return 3

    # Reprise : on repart du ledger (les résolus corrects sont sautés), et tant qu'il
    # reste des challenges non résolus on relance une passe — jusqu'à tout avoir (ou Ctrl-C).
    rows_by_name: dict[str, dict] = {}
    round_no = 0
    force = args.force
    interrupted = False
    try:
        while True:
            round_no += 1
            label = round_no if not args.once else None
            rows_by_name.update(_run_pass(targets, cfg, ledger, force, label))
            force = False  # après la 1re passe, on ne refait plus les déjà-résolus

            remaining = _remaining(targets, ledger)
            if not remaining:
                print(f"\n[✓] Tous les challenges résolus (en {round_no} passe(s)).")
                break
            if args.once:
                break
            if args.max_rounds and round_no >= args.max_rounds:
                print(f"\n[!] {len(remaining)} challenge(s) non résolu(s) après {round_no} passe(s) (--max-rounds).")
                break
            names = ", ".join(f"{c.parent.name}/{c.name}" for c in remaining)
            print(f"\n=== Passe {round_no} finie — {len(remaining)} restant(s), on relance : {names} ===\n", flush=True)
    except KeyboardInterrupt:
        interrupted = True
        print("\n[!] Interrompu (Ctrl-C) — progression sauvegardée dans le ledger ; "
              "relance la commande pour reprendre là où tu t'étais arrêté.")

    # Rapport dans l'ordre des targets, en reflétant l'état le plus récent du ledger.
    rows = []
    for c in targets:
        name = f"{c.parent.name}/{c.name}"
        e = ledger.get(c.parent.name, c.name)
        if e:
            rows.append({"challenge": name, **{k: e.get(k) for k in ("solved", "correct", "flag", "steps", "tokens", "seconds", "reason")}})
        elif name in rows_by_name:
            rows.append(rows_by_name[name])
    _write_report(cfg, rows)
    solved = sum(1 for r in rows if r.get("correct"))
    print(f"\n=== {solved}/{len(rows)} résolus (flag correct) ===")
    return 130 if interrupted else 0


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

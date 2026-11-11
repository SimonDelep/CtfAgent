"""Orchestrateur : prépare le workdir local, câble registre + forge + boucle, journalise.

Usage :
    python -m agent.orchestrator CSAW-Quals/crypto/secret_treaties
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from .config import REPO_ROOT, load_config
from .core.base_tools import register_base_tools
from .core.context import RunContext
from .core.executor import LocalExecutor
from .core.forge import Forge
from .core.ledger import Ledger
from .core.loop import AgentLoop, RunResult
from .core.registry import ToolRegistry
from .core.report import Transcript, generate_writeup
from .core.verifier import FlagVerifier
from .llm_client import LLMClient
from .prompt import build_system_prompt, build_user_prompt


def load_challenge(chal_dir: Path) -> dict:
    meta = json.loads((chal_dir / "challenge.json").read_text(encoding="utf-8"))
    meta["_dir"] = str(chal_dir)
    return meta


def _resolve(p: str | Path) -> Path:
    p = Path(p)
    return p if p.is_absolute() else REPO_ROOT / p


def solve_challenge(chal_dir: Path, cfg: dict, use_ground_truth: bool = True, stream: bool | None = None) -> RunResult:
    meta = load_challenge(chal_dir)
    category = meta.get("category", "misc")

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = _resolve(cfg["paths"]["runs_dir"]) / f"{category}_{chal_dir.name}_{ts}"
    workdir = run_dir / "work"
    run_forge_dir = run_dir / "forge"
    transcript = Transcript(run_dir)

    llm = LLMClient(cfg)
    gt = meta.get("flag") if use_ground_truth else None
    verifier = FlagVerifier(cfg["flag"]["regex"], ground_truth=gt)
    executor = LocalExecutor(workdir, chal_dir, int(cfg["executor"]["default_timeout"]))

    registry = ToolRegistry()
    register_base_tools(registry)
    forge = Forge(registry, run_forge_dir, _resolve(cfg["paths"]["forge_lib"]),
                  shared_lib=bool(cfg["forge"].get("shared_lib", True)))
    forge.register_meta_tools()

    ctx = RunContext(executor=executor, verifier=verifier, registry=registry, forge=forge,
                     transcript=transcript, workdir=workdir, challenge_dir=chal_dir.resolve())

    loop_opts = {
        "stuck_threshold": int(cfg["forge"].get("stuck_threshold", 3)),
        "repeat_threshold": int(cfg.get("loop", {}).get("repeat_threshold", 3)),
        "summary_interval": int(cfg.get("loop", {}).get("summary_interval", 10)),
        "stream": bool(cfg.get("ui", {}).get("stream", True)) if stream is None else stream,
    }
    loop = AgentLoop(llm, ctx, transcript, cfg["budget"], options=loop_opts)
    result = loop.run(build_system_prompt(category), build_user_prompt(meta))

    transcript.log("result", **result.__dict__)
    generate_writeup(llm, meta, transcript, result.flag)
    transcript.close()
    (run_dir / "result.json").write_text(json.dumps(result.__dict__, indent=2, ensure_ascii=False), encoding="utf-8")

    # suivi persistant (reprise sans tout refaire)
    Ledger(_resolve(cfg["paths"]["runs_dir"]) / "ledger.json").update(category, chal_dir.name, result, run_dir)
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description="Résout un challenge CTF avec l'agent autonome.")
    ap.add_argument("challenge", help="Dossier du challenge (contient challenge.json).")
    ap.add_argument("--config", default=None)
    ap.add_argument("--no-ground-truth", action="store_true", help="Mode compét' : flag inconnu.")
    ap.add_argument("--quiet", action="store_true", help="Désactive l'affichage live.")
    args = ap.parse_args(argv)

    cfg = load_config(args.config)
    chal_dir = _resolve(args.challenge)
    if not (chal_dir / "challenge.json").exists():
        print(f"[!] challenge.json introuvable dans {chal_dir}", file=sys.stderr)
        return 2

    if not LLMClient(cfg).ping():
        print(f"[!] Endpoint LLM injoignable: {cfg['llm']['base_url']} "
              f"(lance Ollama et configure LLM_BASE_URL/LLM_MODEL)", file=sys.stderr)
        return 3

    result = solve_challenge(chal_dir, cfg, use_ground_truth=not args.no_ground_truth,
                             stream=not args.quiet)
    print(json.dumps(result.__dict__, indent=2, ensure_ascii=False))
    return 0 if result.solved and (result.correct is not False) else 1


if __name__ == "__main__":
    raise SystemExit(main())

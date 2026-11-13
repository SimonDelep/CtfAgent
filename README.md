# CtfAgent — Autonomous CTF Solver (CSAW LLM 2026)

An agent that solves CTF challenges **with no human in the loop**, driven by a **local model
served through Ollama**, running **directly on the host** (no Docker). For every challenge it
produces an **execution-proven flag**, a full **transcript**, and a **write-up**.

> A detailed French reference lives in [`agent/README.md`](agent/README.md). This file is a
> short English write-up of the **strategy** and **how it is implemented**.

## Strategy

The agent is a **ReAct loop** (think → act → observe) wrapped around four core ideas:

1. **Tool Forge.** When the base tools (`run_shell`, `run_python`, `read_file`,
   `copy_challenge_file`, `submit_flag`) aren't enough, the model **writes or edits its own
   tool on the fly** (`forge_tool` / `edit_tool`). Each forged tool is a standalone Python
   file (`SCHEMA` + `def main(args)`); it is validated, hot-reloaded, and callable on the next
   turn. This lets the agent encapsulate a repeated maneuver (XOR brute-force, LSB extractor,
   replayable network client, LLL solver…) once and reuse it.

2. **Grounded verifier.** A flag is accepted **only if it appears in a real tool output** —
   never from the model's free text. This eliminates hallucinated flags. In evaluation mode a
   known ground-truth flag is required; in competition mode (`--no-ground-truth`) the first
   well-formed flag coming from a tool output is accepted.

3. **Anti-stall control.** An **identical** tool call repeated `repeat_threshold` times (default
   3) is short-circuited (cached result + "change your approach" warning); after
   `stuck_threshold` turns with no useful output, the loop **nudges** the model toward the Forge.

4. **Bounded context via rolling memory.** Every `summary_interval` turns the model writes a
   summary (*Done / Dead-ends / State / Next leads*) that **replaces the detailed history**, so
   the context window never overflows and failed approaches aren't repeated.

Each challenge runs under a **budget** (`max_steps`, `max_tokens_total`, `wall_clock_seconds`);
the first ceiling reached ends the attempt and the harness moves on.

## How it is implemented

```
orchestrator.py    builds runs/<chal>/work, wires everything, launches the loop
  prompt.py          single adaptive prompt (category hint + resume block)
  llm_client.py      OpenAI-compatible client (Ollama) + JSON tool-call fallback + I/O logging
  core/loop.py       ReAct loop, budgets, anti-loop/stuck, rolling cumulative summary
  core/registry.py   unified registry: base (native) + forged tools, active vs library
  core/forge.py      forge_tool / edit_tool / list_tools / search_tools / load_tool
  core/executor.py   LOCAL execution (subprocess, timeout, cwd=work, python3 -I)
  core/verifier.py   grounded flag validation
  core/ledger.py     persistent per-challenge tracking (resume, no-downgrade guard)
  core/report.py     transcript.jsonl + writeup.md
  forge/lib/         shared forged-tool library (reused across challenges)
  eval/run.py        scoring harness (aggregate metrics → report.md)
```

A forged tool is just a file:

```python
SCHEMA = { "name": "...", "description": "...", "parameters": {...} }  # added by the Forge
def main(args):          # written by the LLM; print() == observation returned to the agent
    ...
# standard footer added by the Forge (reads JSON args from argv, calls main)
```

### Key design points added in the latest iteration

- **On-demand tool library.** The shared `forge/lib/` grew to dozens of tools, and exposing all
  of them to the model every turn bloated the context (~47 schemas/turn) and hurt tool
  selection. Now only **base tools + tools forged during the current run** are exposed
  (~10/turn). The shared library is **searchable on demand** via `search_tools(query)` and pulled
  into the active set with `load_tool(name)`. Newly forged tools are active immediately for the
  run and mirrored into the library for future runs.

- **Cross-run resume.** On a retry, the previous attempt's `summary.md` is re-injected into the
  prompt (a `=== RESUME ===` block) so the agent continues from what it already learned instead
  of restarting reconnaissance from scratch. Forged tools from the prior attempt remain reachable
  through the library.

- **Cumulative in-run summary.** Each periodic summary now folds the *previous* cumulative
  summary together with recent events (bounded), so compaction no longer drops older findings —
  it keeps the whole trajectory, compactly.

- **Ledger no-downgrade guard.** A re-attempt that fails can no longer overwrite a previously
  recorded success — a solved flag is never lost by a later budget-exhausted run.

- **Full LLM I/O log.** Each run writes `runs/<chal>/messages/NNNN.json`, one file per LLM call,
  capturing the exact request (all messages sent, tools exposed, params) and the raw response.
  Toggle with `logging.llm_io` in `agent/config.yaml`.

## Usage

```bash
pip install -r agent/requirements.txt         # requests + pyyaml (host side)

# Model config via .env at the project root (copy .env.example -> .env):
#   LLM_BASE_URL=http://localhost:11434/v1
#   LLM_API_KEY=ollama
#   LLM_MODEL=huihui_ai/qwen3.5-abliterated:122b

python -m agent.orchestrator CSAW-Quals/crypto/secret_treaties   # one challenge
python -m agent.eval.run --pilots                                 # one per category
python -m agent.eval.run                                          # full benchmark (resumes;
                                                                  # skips solved, retries fails)
python -m agent.eval.run --status                                 # progress table
```

Outputs per run: `agent/runs/<cat>_<chal>_<ts>/` — `transcript.jsonl`, `writeup.md`,
`summary.md`, `result.json`, `messages/`, `work/`, `forge/`. Aggregate results in
`agent/eval/report.md`; persistent tracking in `agent/runs/ledger.json`.

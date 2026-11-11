"""Chargement de la config YAML avec substitution ${VAR:-default} depuis l'environnement."""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml

_ENV_RE = re.compile(r"\$\{([A-Z0-9_]+)(?::-(.*?))?\}")

AGENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = AGENT_DIR.parent


def load_dotenv(paths: list[Path] | None = None) -> None:
    """Charge un .env (KEY=VALUE) dans os.environ, sans écraser les variables déjà définies.

    Sans dépendance. Cherche, dans l'ordre : csaw/.env puis agent/.env. Ignore les lignes
    vides, les commentaires (#) et le préfixe optionnel `export `. Retire les guillemets.
    """
    if paths is None:
        paths = [REPO_ROOT / ".env", AGENT_DIR / ".env"]
    for path in paths:
        if not path.exists():
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export "):]
            if "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:   # une variable déjà exportée gagne
                os.environ[key] = val


def _expand(value: Any) -> Any:
    if isinstance(value, str):
        def repl(m: re.Match) -> str:
            var, default = m.group(1), m.group(2)
            return os.environ.get(var, default if default is not None else "")
        return _ENV_RE.sub(repl, value)
    if isinstance(value, dict):
        return {k: _expand(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand(v) for v in value]
    return value


def load_config(path: str | Path | None = None) -> dict:
    load_dotenv()  # .env chargé avant la substitution ${VAR:-...}
    path = Path(path) if path else AGENT_DIR / "config.yaml"
    with open(path, "r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    cfg = _expand(raw)
    # Normalise quelques types numériques venant d'une substitution d'env (toujours str).
    cfg.setdefault("budget", {})
    for k in ("max_steps", "max_tokens_total", "wall_clock_seconds"):
        if k in cfg["budget"]:
            cfg["budget"][k] = int(cfg["budget"][k])
    return cfg


if __name__ == "__main__":
    import json
    print(json.dumps(load_config(), indent=2))

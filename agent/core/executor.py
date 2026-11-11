"""Exécuteur LOCAL (pas de Docker) : lance des sous-processus dans un workdir dédié par run.

Isolation légère : cwd = runs/<chal>/work ; interpréteur Python lancé avec `-I` (ignore
l'environnement et les chemins utilisateur) ; les artefacts du challenge restent dans leur
dossier d'origine et sont copiés dans le workdir au besoin (jamais exécutés depuis /chal).
"""
from __future__ import annotations

import json
import subprocess
import uuid
from pathlib import Path


def _truncate(text: str | None, limit: int = 12000) -> str:
    if not text:
        return ""
    if len(text) <= limit:
        return text
    return f"{text[:limit//2]}\n...[{len(text)-limit} octets tronqués]...\n{text[-limit//2:]}"


class LocalExecutor:
    def __init__(self, workdir: Path, challenge_dir: Path, default_timeout: int = 120):
        self.workdir = Path(workdir).resolve()
        self.workdir.mkdir(parents=True, exist_ok=True)
        self.challenge_dir = Path(challenge_dir).resolve()
        self.default_timeout = default_timeout

    def _run(self, argv: list[str], timeout: int | None = None, input_text: str | None = None) -> dict:
        try:
            p = subprocess.run(
                argv, cwd=str(self.workdir), capture_output=True, text=True,
                timeout=timeout or self.default_timeout, input=input_text,
            )
            return {"exit_code": p.returncode, "stdout": _truncate(p.stdout),
                    "stderr": _truncate(p.stderr), "timed_out": False}
        except subprocess.TimeoutExpired as exc:
            return {"exit_code": -1, "stdout": _truncate(exc.stdout or ""),
                    "stderr": "[timeout] " + _truncate(exc.stderr or ""), "timed_out": True}
        except Exception as exc:  # noqa: BLE001
            return {"exit_code": -1, "stdout": "", "stderr": f"[exec error] {exc}", "timed_out": False}

    # --- primitives utilisées par les outils de base ---------------------
    def run_shell(self, command: str, timeout: int | None = None) -> dict:
        return self._run(["bash", "-lc", command], timeout)

    def run_python(self, code: str, timeout: int | None = None) -> dict:
        name = f"_snippet_{uuid.uuid4().hex[:8]}.py"
        (self.workdir / name).write_text(code, encoding="utf-8")
        return self._run(["python3", "-I", name], timeout)

    def run_forged(self, script_path: Path, args: dict, timeout: int | None = None) -> dict:
        """Exécute un outil forgé : python3 -I <script> '<args_json>' (cwd=workdir)."""
        return self._run(["python3", "-I", str(script_path), json.dumps(args)], timeout)

    def read_file(self, path: str, max_bytes: int = 20000) -> dict:
        p = Path(path)
        if not p.is_absolute():
            # cherche d'abord dans le workdir, sinon dans le dossier du challenge
            cand = self.workdir / path
            p = cand if cand.exists() else (self.challenge_dir / path)
        try:
            data = p.read_bytes()[:max_bytes]
            try:
                return {"exit_code": 0, "stdout": data.decode("utf-8", "replace"), "stderr": ""}
            except Exception:  # noqa: BLE001
                return {"exit_code": 0, "stdout": repr(data), "stderr": ""}
        except Exception as exc:  # noqa: BLE001
            return {"exit_code": -1, "stdout": "", "stderr": f"read_file: {exc}"}

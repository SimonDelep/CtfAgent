"""Sandbox ③ — exécution réelle dans un conteneur Docker isolé.

Implémente l'interface `World` pour la *phase réelle*. Chaque action de l'agent
y est exécutée dans un conteneur sans accès Internet, avec timeout et sortie
tronquée, puis renvoyée sous forme d'`Observation`.

⚠️ Ce module **ne lance rien à l'import** et, par sécurité, refuse d'exécuter
tant qu'il n'est pas explicitement activé (`enabled=True`). Le reste du système
(orchestrateur, rêve) fonctionne sans Docker. L'implémentation Docker réelle est
laissée aux agents/intégrateurs : le point d'extension est `_run_in_container`.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from core.types import Action, Observation

MAX_OUTPUT = 4000  # caractères conservés par observation


class SandboxError(RuntimeError):
    pass


class Sandbox:
    """Monde réel. Exécute les actions dans un conteneur isolé.

    Args:
        workspace: dossier du challenge monté dans le conteneur.
        image: image Docker contenant les outils CTF.
        timeout: délai max par commande (s).
        enabled: garde-fou. Tant que False, toute exécution lève SandboxError.
            On ne l'active que lorsqu'on veut réellement attaquer un challenge.
    """

    def __init__(
        self,
        workspace: str | Path,
        *,
        image: str = "ctfagent-sandbox:latest",
        timeout: float = 60.0,
        enabled: bool = False,
        forge=None,
    ) -> None:
        self.workspace = Path(workspace)
        self.image = image
        self.timeout = timeout
        self.enabled = enabled
        # Forgeron d'outils : permet d'exécuter les outils forgés DANS le conteneur.
        self.forge = forge

    def reset(self) -> None:
        """Nouvelle branche : rien à faire ici (conteneur éphémère par commande)."""

    def step(self, action: Action) -> Observation:
        if not self.enabled:
            raise SandboxError(
                "Sandbox désactivée (enabled=False). Active-la explicitement pour "
                "exécuter de vraies commandes Docker."
            )
        # Outil forgé (option 2) : exécuté comme script isolé dans le conteneur.
        if self.forge is not None and self.forge.is_generated(action.tool):
            return self._run_generated(action)
        if action.tool == "run_cmd":
            return self._run_in_container(action.args.get("cmd", ""))
        if action.tool == "python_exec":
            code = action.args.get("code", "")
            return self._run_in_container(f"python3 -c {_shquote(code)}")
        if action.tool == "read_file":
            return self._read_file(action.args.get("path", ""))
        if action.tool == "remote":
            # TODO: brancher pwntools/curl vers le service du challenge.
            return Observation(output="[remote non implémenté]", exit_code=None)
        return Observation(output=f"[tool inconnu: {action.tool}]", exit_code=None)

    def _run_generated(self, action: Action) -> Observation:
        """Exécute un outil forgé : `python3 -I /forge/<name>.py '<json args>'`.

        Le code forgé tourne en mode isolé (-I), sans Internet, avec le magasin
        d'outils monté en lecture seule. Il ne touche jamais l'hôte.
        """
        import json as _json

        payload = _shquote(_json.dumps(action.args, ensure_ascii=False))
        cmd = f"python3 -I {self.forge.container_path(action.tool)} {payload}"
        return self._run_in_container(cmd)

    # -- points d'extension ---------------------------------------------- #
    def _run_in_container(self, cmd: str) -> Observation:
        """Exécute `cmd` dans Docker. À compléter selon l'infra disponible.

        Squelette volontairement prudent : la commande `docker run` est
        construite mais l'exécution réelle dépend des droits Docker de la
        machine. On tronque toujours la sortie.
        """
        docker_cmd = [
            "docker", "run", "--rm", "--network", "none",
            "-v", f"{self.workspace}:/work:ro", "-w", "/work",
        ]
        # Monte le magasin d'outils forgés en lecture seule, le cas échéant.
        if self.forge is not None:
            docker_cmd += ["-v", f"{self.forge.live_dir.resolve()}:{self.forge.container_mount}:ro"]
        docker_cmd += [self.image, "bash", "-lc", cmd]
        try:
            proc = subprocess.run(
                docker_cmd, capture_output=True, text=True, timeout=self.timeout
            )
        except subprocess.TimeoutExpired:
            return Observation(output="[timeout]", exit_code=124, truncated=True)
        except FileNotFoundError as exc:
            raise SandboxError(f"Docker indisponible : {exc}") from exc
        out = (proc.stdout or "") + (proc.stderr or "")
        return _truncate(out, proc.returncode)

    def _read_file(self, rel: str) -> Observation:
        target = (self.workspace / rel).resolve()
        try:
            target.relative_to(self.workspace.resolve())
        except ValueError:
            return Observation(output="[accès refusé hors workspace]", exit_code=1)
        if not target.is_file():
            return Observation(output=f"[fichier introuvable: {rel}]", exit_code=1)
        try:
            data = target.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            return Observation(output=f"[lecture impossible: {exc}]", exit_code=1)
        return _truncate(data, 0)


def _truncate(text: str, code: int | None) -> Observation:
    truncated = len(text) > MAX_OUTPUT
    if truncated:
        text = text[:MAX_OUTPUT] + f"\n[... sortie tronquée à {MAX_OUTPUT} caractères]"
    return Observation(output=text, exit_code=code, truncated=truncated)


def _shquote(s: str) -> str:
    return "'" + s.replace("'", "'\\''") + "'"

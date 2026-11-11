"""Contexte d'exécution passé à chaque handler d'outil (natif ou méta-forge)."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .executor import LocalExecutor
    from .forge import Forge
    from .registry import ToolRegistry
    from .report import Transcript
    from .verifier import FlagVerifier


@dataclass
class RunContext:
    executor: "LocalExecutor"
    verifier: "FlagVerifier"
    registry: "ToolRegistry"
    forge: "Forge"
    transcript: "Transcript"
    workdir: Path
    challenge_dir: Path
    # rempli par la boucle quand un flag 'grounded' est accepté via submit_flag
    accepted_flag: str | None = None

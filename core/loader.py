"""Chargeur de challenge — étape ① du README.

Lit `challenge.json`, construit un workspace isolé contenant UNIQUEMENT l'énoncé
et les fichiers listés pour le joueur, et renvoie un `Challenge`. Les éléments
sensibles (flag attendu, dossiers `solution/`, `solve.py`, `writeup.md`) ne sont
jamais copiés ni exposés : c'est la garde anti-triche du projet.

Tolérant aux variantes de format, car le dépôt NYU-LLM-CTF n'est pas uniforme
d'une année à l'autre (champs `prompt`/`description`, `files`/`attachments`…).
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from core.types import CATEGORIES, DEFAULT_FLAG_REGEX, Challenge

# Noms de fichiers / dossiers à ne jamais exposer à un agent.
SECRET_NAMES = {"solution", "solutions", "solve", "writeup", "writeups", "flag", "flags"}
SECRET_SUFFIXES = {".sol"}
# Clés de challenge.json qui peuvent contenir le flag ou un indice direct.
SECRET_KEYS = {"flag", "flags", "answer", "solution", "solutions"}


def _first(meta: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for k in keys:
        if k in meta and meta[k] not in (None, ""):
            return meta[k]
    return default


def _is_secret_path(name: str) -> bool:
    stem = Path(name).stem.lower()
    low = name.lower()
    if Path(name).suffix.lower() in SECRET_SUFFIXES:
        return True
    return any(s in low for s in SECRET_NAMES) or stem in SECRET_NAMES


def load_challenge(
    challenge_dir: str | Path,
    workspace: str | Path | None = None,
    *,
    copy_files: bool = True,
) -> Challenge:
    """Charge un challenge depuis son dossier.

    Args:
        challenge_dir: dossier contenant `challenge.json`.
        workspace: dossier isolé où copier l'énoncé et les fichiers autorisés.
            Si None, aucun fichier n'est copié (mode lecture seule des métadonnées).
        copy_files: mettre à False pour inspecter sans matérialiser le workspace.

    Returns:
        Un `Challenge` sans aucune donnée secrète.
    """
    challenge_dir = Path(challenge_dir).resolve()
    manifest = challenge_dir / "challenge.json"
    if not manifest.is_file():
        raise FileNotFoundError(f"challenge.json introuvable dans {challenge_dir}")

    meta: dict[str, Any] = json.loads(manifest.read_text(encoding="utf-8"))

    name = str(_first(meta, "name", "title", "challenge", default=challenge_dir.name))
    description = str(
        _first(meta, "description", "prompt", "statement", "text", "body", default="")
    )
    declared = _first(meta, "category", "cat", "type")
    declared_category = str(declared).lower().strip() if declared else None
    if declared_category and declared_category not in CATEGORIES:
        declared_category = _normalise_category(declared_category)

    host = _first(meta, "host", "server", "ip")
    port = _first(meta, "port")
    try:
        port = int(port) if port is not None else None
    except (TypeError, ValueError):
        port = None

    flag_regex = str(_first(meta, "flag_format", "flag_regex", default=DEFAULT_FLAG_REGEX))

    # Liste des fichiers destinés au joueur.
    declared_files = _first(meta, "files", "attachments", "handout", default=[]) or []
    if isinstance(declared_files, str):
        declared_files = [declared_files]

    copied: list[str] = []
    ws: Path | None = None
    if copy_files and workspace is not None:
        ws = Path(workspace).resolve()
        ws.mkdir(parents=True, exist_ok=True)
        copied = _materialise_workspace(challenge_dir, ws, declared_files, description)

    # Métadonnées publiques seulement (on retire toute clé secrète).
    public_meta = {k: v for k, v in meta.items() if k.lower() not in SECRET_KEYS}

    return Challenge(
        name=name,
        description=description,
        declared_category=declared_category,
        files=copied,
        host=str(host) if host else None,
        port=port,
        workspace=ws,
        flag_regex=flag_regex,
        meta=public_meta,
    )


def _materialise_workspace(
    challenge_dir: Path,
    workspace: Path,
    declared_files: list[str],
    description: str,
) -> list[str]:
    """Copie énoncé + fichiers autorisés dans le workspace, rien d'autre."""
    copied: list[str] = []

    # 1. L'énoncé, pour que l'agent y ait accès comme fichier.
    (workspace / "README_challenge.txt").write_text(description, encoding="utf-8")

    # 2. Les fichiers explicitement listés.
    search_roots = [challenge_dir, challenge_dir / "files", challenge_dir / "dist"]
    for rel in declared_files:
        rel = str(rel).strip()
        if not rel or _is_secret_path(rel):
            continue
        src = _resolve_file(rel, search_roots, challenge_dir)
        if src is None:
            continue
        dst = workspace / Path(rel).name
        try:
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            copied.append(dst.name)
        except OSError:
            continue

    # 3. Repli : si rien n'est listé, copier le contenu de files/ ou dist/ en
    #    excluant tout ce qui ressemble à une solution.
    if not declared_files:
        for root in (challenge_dir / "files", challenge_dir / "dist"):
            if not root.is_dir():
                continue
            for item in root.iterdir():
                if _is_secret_path(item.name):
                    continue
                dst = workspace / item.name
                try:
                    if item.is_dir():
                        shutil.copytree(item, dst, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, dst)
                    copied.append(dst.name)
                except OSError:
                    continue

    return sorted(set(copied))


def _resolve_file(rel: str, roots: list[Path], base: Path) -> Path | None:
    """Trouve un fichier listé en restant sous le dossier du challenge."""
    for root in roots:
        cand = (root / rel).resolve()
        # Interdit de remonter hors du dossier du challenge.
        try:
            cand.relative_to(base)
        except ValueError:
            continue
        if cand.exists():
            return cand
    # Recherche par nom de base en dernier recours.
    name = Path(rel).name
    for match in base.rglob(name):
        if _is_secret_path(str(match.relative_to(base))):
            continue
        return match
    return None


def _normalise_category(raw: str) -> str | None:
    """Ramène des libellés variés vers les six catégories canoniques."""
    raw = raw.lower()
    alias = {
        "web": "web",
        "crypto": "crypto",
        "cryptography": "crypto",
        "rev": "rev",
        "reverse": "rev",
        "reversing": "rev",
        "re": "rev",
        "pwn": "pwn",
        "binary": "pwn",
        "binary exploitation": "pwn",
        "exploitation": "pwn",
        "forensics": "forensics",
        "forensic": "forensics",
        "stego": "forensics",
        "steganography": "forensics",
        "misc": "misc",
        "miscellaneous": "misc",
    }
    if raw in alias:
        return alias[raw]
    for key, val in alias.items():
        if key in raw:
            return val
    return None

"""Outils de BASE (natifs) + enregistrement dans le registre.

run_shell / run_python / read_file / copy_challenge_file / submit_flag.
Les méta-outils de la forge (forge_tool/edit_tool/list_tools) sont ajoutés par forge.py.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from .registry import ToolRegistry


def _schema(name, desc, props, required):
    return {"name": name, "description": desc,
            "parameters": {"type": "object", "properties": props, "required": required}}


# --- handlers ------------------------------------------------------------
def _run_shell(args, ctx):
    return ctx.executor.run_shell(args["command"], args.get("timeout"))


def _run_python(args, ctx):
    return ctx.executor.run_python(args["code"], args.get("timeout"))


def _read_file(args, ctx):
    return ctx.executor.read_file(args["path"], args.get("max_bytes", 20000))


def _copy_challenge_file(args, ctx):
    rel = args["rel"]
    src = ctx.challenge_dir / rel
    dst = ctx.workdir / (args.get("dest") or Path(rel).name)
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return {"exit_code": 0, "stdout": f"copié {src} -> {dst}", "stderr": ""}
    except Exception as exc:  # noqa: BLE001
        return {"exit_code": -1, "stdout": "", "stderr": f"copy: {exc}"}


def _submit_flag(args, ctx):
    flag = str(args.get("flag", "")).strip()
    verdict = ctx.verifier.validate(flag)
    if verdict["accepted"]:
        ctx.accepted_flag = flag
    else:
        verdict["hint"] = ("Flag REFUSÉ : il n'apparaît dans AUCUNE sortie d'outil réelle. "
                           "Ne devine pas — produis-le via une exécution (outil de base ou forgé).")
    return verdict


# --- enregistrement ------------------------------------------------------
def register_base_tools(reg: ToolRegistry) -> None:
    reg.register_native(_schema(
        "run_shell", "Exécute une commande bash dans le workdir du run. Renvoie exit_code/stdout/stderr.",
        {"command": {"type": "string"}, "timeout": {"type": "integer"}}, ["command"]), _run_shell)

    reg.register_native(_schema(
        "run_python", "Exécute un script Python3 (isolé -I) dans le workdir. Utilise print() pour voir les résultats.",
        {"code": {"type": "string"}, "timeout": {"type": "integer"}}, ["code"]), _run_python)

    reg.register_native(_schema(
        "read_file", "Lit les premiers octets d'un fichier (workdir, dossier du challenge, ou chemin absolu).",
        {"path": {"type": "string"}, "max_bytes": {"type": "integer"}}, ["path"]), _read_file)

    reg.register_native(_schema(
        "copy_challenge_file", "Copie un fichier du challenge vers le workdir pour le manipuler.",
        {"rel": {"type": "string"}, "dest": {"type": "string"}}, ["rel"]), _copy_challenge_file)

    reg.register_native(_schema(
        "submit_flag", "Soumet un flag. À n'appeler QUE si le flag provient d'une sortie d'outil réelle.",
        {"flag": {"type": "string"}}, ["flag"]), _submit_flag)

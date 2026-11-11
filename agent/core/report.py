"""Journalisation : transcript.jsonl (pièce maîtresse de la soumission) + write-up auto."""
from __future__ import annotations

import json
import time
from pathlib import Path


class Transcript:
    def __init__(self, run_dir: Path):
        self.run_dir = Path(run_dir)
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.run_dir / "transcript.jsonl"
        self._fh = open(self.path, "w", encoding="utf-8")
        self.events: list[dict] = []

    def log(self, role: str, **fields) -> None:
        event = {"ts": round(time.time(), 3), "role": role, **fields}
        self.events.append(event)
        self._fh.write(json.dumps(event, ensure_ascii=False) + "\n")
        self._fh.flush()

    def close(self) -> None:
        if not self._fh.closed:
            self._fh.close()


WRITEUP_PROMPT = """Tu es l'agent CTF. La trajectoire ci-dessous est ton historique complet de
résolution d'un challenge. Rédige un write-up concis et clair en français (format Markdown) avec :

1. **Challenge** : nom, catégorie, résumé en une ligne.
2. **Vulnérabilité / mécanique** : la faille ou l'astuce exploitée.
3. **Étapes de résolution** : les étapes clés, avec les outils/commandes décisifs.
4. **Flag** : le flag récupéré.

Reste factuel : ne décris que ce qui s'est réellement passé dans la trajectoire.

Trajectoire :
{trajectory}
"""


def generate_writeup(llm, challenge_meta: dict, transcript: Transcript, flag: str | None) -> str:
    """Un dernier appel LLM qui résume la trajectoire en write-up."""
    lines = []
    for ev in transcript.events:
        role = ev.get("role")
        if role == "assistant" and ev.get("content"):
            lines.append(f"[LLM] {ev['content'][:800]}")
        elif role == "tool_call":
            lines.append(f"[APPEL {ev.get('name')}] {json.dumps(ev.get('arguments', {}), ensure_ascii=False)[:400]}")
        elif role == "tool_result":
            lines.append(f"[RESULTAT] {str(ev.get('result', ''))[:600]}")
    trajectory = "\n".join(lines)[:16000]

    header = (
        f"# Write-up — {challenge_meta.get('name')} ({challenge_meta.get('category')})\n\n"
        f"- **Flag** : `{flag or 'NON TROUVÉ'}`\n\n"
    )
    try:
        resp = llm.chat(
            [
                {"role": "system", "content": "Tu rédiges des write-ups CTF précis et honnêtes."},
                {"role": "user", "content": WRITEUP_PROMPT.format(trajectory=trajectory)},
            ],
            temperature=0.3,
        )
        body = resp.content or "(génération du write-up vide)"
    except Exception as exc:  # noqa: BLE001
        body = f"(write-up LLM indisponible : {exc})\n\nTrajectoire brute :\n\n```\n{trajectory[:4000]}\n```"

    text = header + body
    (transcript.run_dir / "writeup.md").write_text(text, encoding="utf-8")
    return text

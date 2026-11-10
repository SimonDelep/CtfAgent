"""Réflecteur ⑨ — transforme les rêves en modifications de stratégie.

À partir des `Dream` jugés, produit **au plus 3** `PolicyEdit`, chacune
justifiée. Un filtre anti-fuite rejette toute modification qui laisserait passer
un nom de challenge précis ou un flag : la stratégie doit rester générique.

L'écriture des éditions peut être confiée au LLM (meilleures reformulations) ;
sans LLM, un repli déterministe ajoute les leçons aux heuristiques. Dans les
deux cas, le filtre anti-fuite s'applique en dernier.
"""
from __future__ import annotations

import re

from core.llm import LLMClient, LLMError
from core.types import Candidate, Dream, Policy, PolicyEdit

MAX_EDITS = 3

# Motifs interdits dans une stratégie (fuite d'information de test).
_FLAG_RE = re.compile(r"[A-Za-z0-9_]*\{[^}]*\}")


def _bump_version(version: str) -> str:
    m = re.match(r"v(\d+)", version)
    n = int(m.group(1)) + 1 if m else 1
    return f"v{n}"


class Reflector:
    """Génère une stratégie candidate à partir des rêves."""

    def __init__(self, llm: LLMClient | None = None, *, challenge_names: list[str] | None = None) -> None:
        self.llm = llm
        # Noms de challenges à bannir des stratégies (anti-fuite).
        self.banned = [c.lower() for c in (challenge_names or [])]

    def reflect(self, policy: Policy, dreams: list[Dream]) -> Candidate:
        """Renvoie une candidate v(n+1) ; vide si aucun rêve n'apporte de leçon."""
        useful = [d for d in dreams if d.lesson.strip()]
        useful.sort(key=lambda d: d.score, reverse=True)
        useful = useful[:MAX_EDITS]

        candidate = Candidate(from_version=policy.version, version=_bump_version(policy.version))
        if not useful:
            return candidate

        lessons = [self._sanitise(d.lesson) for d in useful]
        lessons = [l for l in lessons if l]  # retire ce que le filtre a vidé

        if self.llm is not None:
            new_heur = self._rewrite_with_llm(policy, lessons)
        else:
            new_heur = self._append_lessons(policy.heuristics, lessons)

        new_heur = self._sanitise(new_heur)
        if new_heur and new_heur.strip() != policy.heuristics.strip():
            candidate.edits.append(PolicyEdit(
                target="heuristics",
                rationale="Leçons issues des mauvaises bifurcations rêvées : "
                          + " | ".join(lessons[:MAX_EDITS]),
                new_content=new_heur,
            ))
        return candidate

    # -- anti-fuite ------------------------------------------------------- #
    def _sanitise(self, text: str) -> str:
        """Retire flags et noms de challenges ; renvoie '' si irrécupérable."""
        if not text:
            return ""
        cleaned = _FLAG_RE.sub("«flag»", text)
        low = cleaned.lower()
        for name in self.banned:
            if name and name in low:
                # On retire la phrase contenant le nom plutôt que tout jeter.
                cleaned = _drop_sentences_with(cleaned, name)
        return cleaned.strip()

    # -- écriture des heuristiques --------------------------------------- #
    def _append_lessons(self, heuristics: str, lessons: list[str]) -> str:
        block = "\n".join(f"- {l}" for l in lessons)
        base = heuristics.rstrip()
        marker = "## Leçons apprises (rêve)"
        if marker in base:
            return base + "\n" + block
        return f"{base}\n\n{marker}\n{block}".lstrip()

    def _rewrite_with_llm(self, policy: Policy, lessons: list[str]) -> str:
        sys = (
            "Tu améliores une stratégie GÉNÉRIQUE de résolution de CTF. On te donne "
            "les heuristiques actuelles et des leçons tirées de tentatives passées. "
            "Réécris les heuristiques en intégrant les leçons, en restant générique : "
            "JAMAIS de nom de challenge, JAMAIS de flag. Réponds par le Markdown seul."
        )
        user = (
            "Heuristiques actuelles :\n---\n" + (policy.heuristics or "(vides)") +
            "\n---\nLeçons à intégrer :\n" + "\n".join(f"- {l}" for l in lessons)
        )
        try:
            return self.llm.chat(
                [{"role": "system", "content": sys}, {"role": "user", "content": user}],
                max_tokens=800,
            )
        except LLMError:
            return self._append_lessons(policy.heuristics, lessons)


def _drop_sentences_with(text: str, needle: str) -> str:
    keep = [s for s in re.split(r"(?<=[.\n])", text) if needle not in s.lower()]
    return "".join(keep)

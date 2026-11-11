"""Réflecteur ⑨ — transforme l'expérience en modifications de stratégie.

Trois sources de leçons, par ordre de priorité :
  1. **Échecs** : le LLM relit la trace d'un challenge raté et dit où l'agent a
     bloqué et quelle règle générale aurait aidé (vise « plus de flags ») ;
  2. **Solutions officielles** (entraînement seulement) : la trace ratée est
     comparée au write-up pour en tirer une méthode générale ;
  3. **Rêves** : raccourcis et branches abandonnées (vise « moins d'étapes »).

Les leçons sont fusionnées en **au plus 3** `PolicyEdit`, chacune
justifiée. Un filtre anti-fuite rejette toute modification qui laisserait passer
un nom de challenge précis ou un flag : la stratégie doit rester générique.

L'écriture des éditions peut être confiée au LLM (meilleures reformulations) ;
sans LLM, un repli déterministe ajoute les leçons aux heuristiques. Dans les
deux cas, le filtre anti-fuite s'applique en dernier.
"""
from __future__ import annotations

import re

from core.llm import LLMClient, LLMError
from core.trace import get_tracer
from dataclasses import dataclass

from core.types import Candidate, Dream, Policy, PolicyEdit

MAX_EDITS = 3
# Max number of lessons merged into one new version (keeps heuristics short)
MAX_LESSONS = 6


@dataclass
class FailureCase:
    """Un challenge raté, tel que le réflecteur le voit.
    `writeup` n'est rempli que pour l'ensemble d'ENTRAÎNEMENT.
    """
    challenge_name: str
    trace: str
    writeup: str = ""

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

    def reflect(self, policy: Policy, dreams: list[Dream],
                failure_lessons: list[str] | None = None) -> Candidate:
        """Renvoie une candidate v(n+1) ; vide si rien n'apporte de leçon.

        `failure_lessons` : leçons déjà tirées des échecs (voir `learn_from_failure`),
        prioritaires sur celles des rêves.
        """
        useful = [d for d in dreams if d.lesson.strip()]
        useful.sort(key=lambda d: d.score, reverse=True)

        candidate = Candidate(from_version=policy.version, version=_bump_version(policy.version))
        t = get_tracer()
        # Failures first (more flags), then dreams (fewer steps); no duplicates
        raw = list(failure_lessons or []) + [d.lesson for d in useful]
        lessons: list[str] = []
        for lesson in raw:
            clean = self._sanitise(lesson)
            if clean and clean not in lessons:
                lessons.append(clean)
        lessons = lessons[:MAX_LESSONS]
        if not lessons:
            t.event("reflect", "Aucune leçon exploitable (échecs ni rêves) : pas de candidate")
            return candidate
        t.event("reflect", f"{len(lessons)} leçon(s) retenue(s) "
                           f"({len(failure_lessons or [])} d'échecs, {len(useful)} de rêves)",
                lessons="\n".join(f"- {l}" for l in lessons))

        if self.llm is not None:
            new_heur = self._rewrite_with_llm(policy, lessons)
        else:
            new_heur = self._append_lessons(policy.heuristics, lessons)

        new_heur = self._sanitise(new_heur)
        if new_heur and new_heur.strip() != policy.heuristics.strip():
            candidate.edits.append(PolicyEdit(
                target="heuristics",
                rationale="Leçons issues des échecs et des rêves : "
                          + " | ".join(lessons),
                new_content=new_heur,
            ))
        # What the reflection gives
        if candidate.edits:
            for edit in candidate.edits:
                t.event("reflect", f"{policy.version} → {candidate.version} : édition de "
                                   f"'{edit.target}'", rationale=edit.rationale,
                        new_content=edit.new_content)
        else:
            t.event("reflect", "Les leçons ne changent pas les heuristiques : pas d'édition")
        return candidate

    # -- échecs ----------------------------------------------------------- #
    def learn_from_failure(self, case: FailureCase) -> list[str]:
        """Demande au LLM 1 à 2 leçons générales tirées d'un challenge raté.

        Avec un write-up (entraînement seulement), le LLM compare ce que l'agent
        a fait à la bonne approche. Sans LLM, aucune leçon (une trace ratée ne
        dit rien d'utile sans interprétation).
        """
        t = get_tracer()
        if self.llm is None:
            return []
        sys_msg = (
            "Tu analyses l'échec d'un agent autonome de CTF pour améliorer sa MÉTHODE "
            "générale. Identifie où il a bloqué (piste fausse, boucle, outil mal "
            "utilisé, abandon trop tôt…) et propose 1 ou 2 règles GÉNÉRALES et "
            "actionnables, valables pour d'autres challenges. JAMAIS de nom de "
            "challenge, de nom de fichier précis ni de flag. Réponds en JSON strict : "
            '{"blocage": "<où il a bloqué>", "lessons": ["<règle>", ...]}'
        )
        user = f"## Trace de l'agent (échec)\n{case.trace}"
        if case.writeup:
            user += ("\n\n## Solution officielle (référence, à NE PAS recopier)\n"
                     + case.writeup + "\n\nCompare l'approche de l'agent à la "
                     "solution : quelle méthode générale lui a manqué ?")
        try:
            obj = self.llm.complete_json(
                [{"role": "system", "content": sys_msg}, {"role": "user", "content": user}],
                max_tokens=2048)
        except LLMError as exc:
            t.event("block", f"Réflexion sur l'échec impossible : {exc}")
            return []
        lessons = [str(l) for l in (obj.get("lessons") or []) if str(l).strip()][:2]
        t.event("reflect", f"Échec analysé{' (avec la solution)' if case.writeup else ''} : "
                           f"{obj.get('blocage', '?')}", lessons="\n".join(lessons))
        return lessons

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

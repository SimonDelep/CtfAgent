"""Verifier 'grounded' : un flag n'est valide que s'il apparaît dans une sortie d'OUTIL.

Principe anti-hallucination : on n'accepte jamais un flag qui n'existe que dans le texte
libre du LLM. On ne regarde que les observations (stdout/stderr/fichiers) produites par
l'exécution réelle d'outils dans le sandbox.
"""
from __future__ import annotations

import re


class FlagVerifier:
    def __init__(self, flag_regex: str, ground_truth: str | None = None):
        self.pattern = re.compile(flag_regex)
        self.ground_truth = ground_truth.strip() if ground_truth else None
        self._seen_observations: list[str] = []

    def observe(self, text: str) -> None:
        """Enregistre une sortie d'outil comme source d'évidence recevable."""
        if text:
            self._seen_observations.append(text)

    def extract(self, text: str) -> list[str]:
        if not text:
            return []
        return self.pattern.findall(text)

    def is_grounded(self, flag: str) -> bool:
        """Le flag doit apparaître tel quel dans au moins une observation enregistrée."""
        flag = flag.strip()
        return any(flag in obs for obs in self._seen_observations)

    def candidates_from_observations(self) -> list[str]:
        out: list[str] = []
        for obs in self._seen_observations:
            out.extend(self.pattern.findall(obs))
        # dédoublonne en gardant l'ordre
        seen: set[str] = set()
        uniq = []
        for f in out:
            if f not in seen:
                seen.add(f)
                uniq.append(f)
        return uniq

    def validate(self, flag: str) -> dict:
        """Résultat structuré. En mode éval, compare à la vérité-terrain."""
        flag = flag.strip()
        grounded = self.is_grounded(flag)
        well_formed = bool(self.pattern.fullmatch(flag) or self.pattern.search(flag))
        accepted = grounded and well_formed
        result = {
            "flag": flag,
            "well_formed": well_formed,
            "grounded": grounded,
            "accepted": accepted,
        }
        if self.ground_truth is not None:
            # Mode éval/entraînement : on connaît le vrai flag → on n'accepte QUE lui.
            # Un flag-bidon 'grounded' (ex. csaw{test_flag} présent dans les fichiers)
            # ne doit pas court-circuiter la résolution : l'agent doit continuer.
            correct = flag == self.ground_truth
            result["correct"] = correct
            result["accepted"] = accepted and correct
        return result

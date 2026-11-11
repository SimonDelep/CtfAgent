"""Rêveur + juge ⑧ — apprend des tentatives résolues, hors ligne.

Deux sortes de rêves pour une tentative *résolue* :

1. **Branches abandonnées** (sans LLM pour le jugement) : chaque mauvaise
   bifurcation de l'arbre (hypothèse abandonnée) est jugée — combien d'étapes
   a-t-elle gaspillées ?
2. **Vrais rêves** (avec LLM) : depuis quelques états du chemin gagnant, on
   relance l'agent dans un `MemorySimulator` (monde rejoué, sans vrai
   service). Le juge regarde s'il atteint le résultat en MOINS d'étapes que le
   parcours réel : c'est un raccourci.

Un flag *rêvé* ne compte jamais comme une vraie résolution. Les leçons sont
formulées par le LLM quand il est disponible (sinon, gabarit déterministe),
puis nettoyées par le réflecteur ⑨ (anti-fuite).
"""
from __future__ import annotations

from typing import Callable

import re

from core.llm import LLMError
from core.trace import get_tracer
from core.tree import SearchTree
from core.types import Attempt, Challenge, Dream, Node, Policy
from dream.simulator import MemorySimulator, norm_key
from dream.traces import attempt_trace, transcript_text

# Un juge prend (arbre, nœud de bifurcation, nœud final rêvé) et renvoie
# (rejoint_le_chemin_gagnant, étapes_pour_rejoindre, score, leçon).
JudgeFn = Callable[[SearchTree, Node, Node], tuple[bool, int | None, float, str]]


def default_judge(tree: SearchTree, fork: Node, reached: Node) -> tuple[bool, int | None, float, str]:
    """Juge déterministe : la branche partant de la bifurcation rejoint-elle le
    chemin gagnant ?

    On ne regarde que les **descendants stricts** de la bifurcation : son parent
    est sur le chemin gagnant par construction, il ne compte pas. Dans un arbre,
    une bifurcation ne rejoint jamais le chemin par simple identité de nœud ;
    ce cas sert surtout au rêveur qui rejoue de NOUVELLES actions via le
    simulateur ⑦ et peut retomber sur un état gagnant.
    """
    path = tree.path_to_root(reached.id)  # racine → … → fork → … → reached
    idx = next((i for i, n in enumerate(path) if n.id == fork.id), None)
    descendants = path[idx + 1:] if idx is not None else path
    rejoin = next((n for n in descendants if n.on_solution_path), None)
    if rejoin is not None:
        steps = sum(1 for n in descendants if not n.on_solution_path) + 1
        return True, steps, 1.0 / (1 + steps), (
            "Depuis cette bifurcation, une suite d'actions rejoint le chemin "
            "gagnant ; privilégier ce raccourci."
        )
    wasted = len(descendants) + 1  # étapes dépensées en pure perte
    hyp = fork.hypothesis or (fork.action.tool if fork.action else "?")
    return False, None, 1.0 / (2 + wasted), (
        f"Piste abandonnée « {hyp} » : {wasted} étape(s) perdue(s). Avant de "
        f"s'engager sur une piste, vérifier vite un indice qui la confirme."
    )


class Dreamer:
    """Juge les branches abandonnées et fait de vrais rêves depuis le chemin gagnant."""

    def __init__(self, tree: SearchTree, judge_fn: JudgeFn | None = None, *,
                 llm=None, agent=None, n_starts: int = 3, max_steps: int = 6) -> None:
        self.tree = tree
        self.judge = judge_fn or default_judge
        # LLM to phrase lessons; agent to really dream (both optional)
        self.llm = llm
        self.agent = agent
        self.n_starts = n_starts
        self.max_steps = max_steps

    def dream_attempt(self, attempt_id: str, challenge_name: str, *,
                      challenge: Challenge | None = None,
                      policy: Policy | None = None) -> list[Dream]:
        """Produit les rêves d'une tentative résolue.

        Sans `challenge`/`policy`/agent, seules les branches abandonnées sont
        jugées (mode ancré sur l'arbre, sans relancer l'agent).
        """
        dreams: list[Dream] = []
        # Dreams are written into the challenge's own log file
        t = get_tracer()
        t.start_challenge(challenge_name, attempt=attempt_id)

        # 1. Abandoned branches already in the tree
        forks = self.tree.bad_forks(attempt_id)
        t.event("dream", f"{len(forks)} branche(s) abandonnée(s) à juger")
        for fork in forks:
            reached = _deepest(self.tree, fork)
            rejoined, steps, score, lesson = self.judge(self.tree, fork, reached)
            what = f"{fork.action.tool} {fork.action.args}" if fork.action else "?"
            verdict = (f"rejoint le chemin gagnant en {steps} étape(s)" if rejoined
                       else "impasse")
            # Let the LLM turn the dead branch into a concrete, generic lesson
            if not rejoined and self.llm is not None:
                lesson = self._llm_lesson(
                    "Voici une tentative RÉUSSIE d'un challenge CTF, dont une branche "
                    f"(nœud {fork.id}, profondeur {fork.depth}) a été abandonnée.",
                    attempt_trace(self.tree, attempt_id),
                    "Quelle règle GÉNÉRALE aurait évité d'explorer cette branche, ou "
                    "permis de l'abandonner plus tôt ?") or lesson
            t.event("dream", f"Branche n°{fork.id} : {what} → {verdict} (score {score:.2f})",
                    hypothesis=fork.hypothesis, reached_node=reached.id, lesson=lesson)
            dreams.append(Dream(
                branch_node_id=fork.id,
                challenge_name=challenge_name,
                rejoined_solution_path=rejoined,
                steps_to_rejoin=steps,
                score=score,
                lesson=lesson,
            ))

        # 2. Real dreams: restart the model from states of the winning path
        attempt = self.tree.get_attempt(attempt_id)
        if (self.agent is not None and self.agent.llm is not None and challenge is not None
                and policy is not None and attempt is not None and attempt.solution_leaf_id):
            dreams.extend(self._real_dreams(attempt, challenge, policy))
        else:
            t.event("dream", "Vrais rêves désactivés (pas d'agent / de LLM / de challenge)")

        t.end_challenge()
        return dreams

    # -- vrais rêves ------------------------------------------------------ #
    def _real_dreams(self, attempt: Attempt, challenge: Challenge, policy: Policy) -> list[Dream]:
        t = get_tracer()
        path = self.tree.path_to_root(attempt.solution_leaf_id)  # root → … → flag
        leaf = path[-1]
        starts = self._pick_starts(attempt.id, path)
        t.event("dream", f"{len(starts)} rêve(s) depuis le chemin gagnant "
                         f"(chemin gagnant : {leaf.depth} étapes)")
        world = MemorySimulator(self.tree, attempt.id)
        dreams: list[Dream] = []

        for start in starts:
            prefix = path[: path.index(start) + 1]
            real_left = leaf.depth - start.depth  # steps the real run needed from here
            t.event("dream", f"Rêve depuis le nœud {start.id} (profondeur {start.depth}, "
                             f"{real_left} étape(s) jusqu'au flag sur le chemin gagnant)")
            transcript = self.agent.dream(challenge, policy, world, prefix,
                                          max_steps=self.max_steps)

            # Judge: compare the dream to the rest of the real winning path
            later = {norm_key(n.action): n for n in path[path.index(start) + 1:] if n.action}
            reached_flag, best, used = False, None, None
            for i, (action, obs) in enumerate(transcript, start=1):
                if re.search(challenge.flag_regex, obs.output or "") and not obs.unsimulated:
                    reached_flag, used = True, i
                    break
                node = later.get(norm_key(action))
                if node is not None and (best is None or node.depth > best.depth):
                    best, used = node, i

            if reached_flag:
                gain = real_left - used
                verdict = f"atteint le flag en {used} étape(s) au lieu de {real_left}"
            elif best is not None:
                gain = (best.depth - start.depth) - used
                verdict = (f"rejoint le chemin gagnant (nœud {best.id}) en {used} "
                           f"étape(s) au lieu de {best.depth - start.depth}")
            else:
                gain = None
                verdict = "n'a pas retrouvé le chemin gagnant"
            rejoined = gain is not None
            # Score: a real shortcut is worth more than just rejoining
            score = (1.0 + gain / max(real_left, 1)) if rejoined and gain > 0 else \
                    (0.3 if rejoined else 0.05)

            lesson = ""
            if rejoined and gain > 0:
                lesson = self._shortcut_lesson(attempt.id, start, transcript, used, gain)
            t.event("dream", f"Résultat : {verdict}"
                             + (f" → raccourci de {gain} étape(s) !" if rejoined and gain > 0 else ""),
                    score=f"{score:.2f}", transcript=transcript_text(transcript), lesson=lesson)
            dreams.append(Dream(
                branch_node_id=start.id,
                challenge_name=challenge.name,
                rejoined_solution_path=rejoined,
                steps_to_rejoin=used if rejoined else None,
                score=score,
                transcript=transcript,
                lesson=lesson,
            ))
        return dreams

    def _pick_starts(self, attempt_id: str, path: list[Node]) -> list[Node]:
        """Choisit les états de départ : d'abord là où l'agent a bifurqué, puis
        les plus anciens du chemin (plus grand potentiel de raccourci)."""
        on_path = [n for n in path[:-1] if n.action is not None or n.parent_id is None]
        fork_parents = {f.parent_id for f in self.tree.bad_forks(attempt_id)}
        ordered = [n for n in on_path if n.id in fork_parents] + \
                  [n for n in on_path if n.id not in fork_parents]
        # Skip the state right before the flag: nothing to shorten there
        ordered = [n for n in ordered if n.depth < path[-1].depth - 1]
        return ordered[: self.n_starts]

    # -- leçons ------------------------------------------------------------ #
    def _shortcut_lesson(self, attempt_id: str, start: Node, transcript, used: int,
                         gain: int) -> str:
        dreamed = [a.tool for a, _ in transcript[:used]]
        fallback = (f"Raccourci trouvé en rêve : depuis l'état atteint, enchaîner "
                    f"{' → '.join(dreamed)} suffit ({gain} étape(s) de moins que le "
                    f"parcours réel).")
        if self.llm is None:
            return fallback
        return self._llm_lesson(
            "Voici une tentative RÉUSSIE d'un challenge CTF, puis un rêve qui, "
            f"depuis le nœud {start.id}, atteint le même résultat en {gain} étape(s) "
            "de moins.",
            attempt_trace(self.tree, attempt_id) + "\n\n## Rêve\n" +
            transcript_text(transcript[:used]),
            "Quelle règle GÉNÉRALE permettrait de prendre ce raccourci directement ?"
        ) or fallback

    def _llm_lesson(self, intro: str, trace: str, question: str) -> str:
        """Demande au LLM UNE leçon générique (une phrase), ou '' si échec."""
        sys_msg = ("Tu tires des leçons de méthode pour un agent de CTF. Réponds par "
                   "UNE seule règle générale et actionnable (une ou deux phrases), "
                   "sans nom de challenge, sans nom de fichier précis, sans flag.")
        try:
            out = self.llm.chat([
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": f"{intro}\n\n{trace}\n\n{question}"},
            ], max_tokens=2048)
        except LLMError as exc:
            get_tracer().event("block", f"Leçon LLM impossible : {exc}")
            return ""
        return out.strip()


def _deepest(tree: SearchTree, node: Node) -> Node:
    """Descend jusqu'à une feuille en suivant le premier enfant (branche réelle)."""
    cur = node
    while True:
        kids = tree.children(cur.id)
        if not kids:
            return cur
        cur = kids[0]

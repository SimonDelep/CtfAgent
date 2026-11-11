"""Rêveur + juge ⑧ — apprend des mauvaises bifurcations, hors ligne.

Pour une tentative *résolue*, on repère les mauvaises bifurcations (un bon état
d'où l'agent est parti dans une mauvaise direction). Depuis chacune, le rêveur
relance l'agent dans le simulateur ⑦ et le juge note la branche :
  - a-t-elle rejoint le chemin gagnant, et en combien d'étapes ?
  - un flag *rêvé* ne compte jamais comme une vraie résolution.

Le résultat est une liste de `Dream` que le réflecteur ⑨ transforme en leçons.

Implémentation minimale : le juge est ici déterministe (il compare la position
atteinte au chemin gagnant connu dans l'arbre). Un juge LLM plus fin peut être
branché via `judge_fn`.
"""
from __future__ import annotations

from typing import Callable

from core.trace import get_tracer
from core.tree import SearchTree
from core.types import Dream, Node

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
    return False, None, 1.0 / (2 + wasted), (
        "Cette bifurcation s'éloigne de la solution et gaspille des étapes ; "
        "apprendre à l'éviter tôt."
    )


class Dreamer:
    """Relance l'agent depuis les mauvaises bifurcations et fait juger."""

    def __init__(self, tree: SearchTree, judge_fn: JudgeFn | None = None) -> None:
        self.tree = tree
        self.judge = judge_fn or default_judge

    def dream_attempt(self, attempt_id: str, challenge_name: str) -> list[Dream]:
        """Produit un rêve par mauvaise bifurcation de la tentative résolue.

        Mode « ancré sur l'arbre » : on juge directement les branches déjà
        explorées (sans relancer de LLM). Pour rêver de branches *nouvelles*,
        brancher un agent sur un `Simulator` démarré à `fork.id` et juger le
        nœud atteint — l'interface est prête (voir `dream.simulator`).
        """
        dreams: list[Dream] = []
        # Dreams are written into the challenge's own log file
        t = get_tracer()
        t.start_challenge(challenge_name, attempt=attempt_id)
        forks = self.tree.bad_forks(attempt_id)
        t.event("dream", f"{len(forks)} mauvaise(s) bifurcation(s) à rejouer")
        for fork in forks:
            reached = _deepest(self.tree, fork)
            rejoined, steps, score, lesson = self.judge(self.tree, fork, reached)
            # What it dreams and what it gives
            what = f"{fork.action.tool} {fork.action.args}" if fork.action else "?"
            verdict = (f"rejoint le chemin gagnant en {steps} étape(s)" if rejoined
                       else "impasse")
            t.event("dream", f"Bifurcation n°{fork.id} : {what} → {verdict} (score {score:.2f})",
                    hypothesis=fork.hypothesis, reached_node=reached.id, lesson=lesson)
            dreams.append(Dream(
                branch_node_id=fork.id,
                challenge_name=challenge_name,
                rejoined_solution_path=rejoined,
                steps_to_rejoin=steps,
                score=score,
                lesson=lesson,
            ))
        t.end_challenge()
        return dreams


def _deepest(tree: SearchTree, node: Node) -> Node:
    """Descend jusqu'à une feuille en suivant le premier enfant (branche réelle)."""
    cur = node
    while True:
        kids = tree.children(cur.id)
        if not kids:
            return cur
        cur = kids[0]

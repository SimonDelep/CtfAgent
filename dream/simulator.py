"""Simulateur ⑦ — rejoue le monde à partir de l'arbre, hors ligne.

Implémente l'interface `World` pour la *phase de rêve*. Aucun vrai service n'est
contacté : une action déjà vue dans l'arbre renvoie l'observation enregistrée ;
une action inconnue renvoie `[NON SIMULÉ]` (`Observation.unsimulated=True`).

Ainsi l'agent peut être relancé depuis n'importe quel nœud sans effet de bord,
et sans jamais « inventer » un flag : un flag rêvé ne sort du simulateur que
s'il a réellement été observé dans l'arbre.
"""
from __future__ import annotations

from core.tree import SearchTree
from core.types import Action, Node, Observation, World


class Simulator(World):
    """Monde de rêve ancré sur une tentative enregistrée.

    Le simulateur suit une position courante dans l'arbre. `step(action)` :
      - cherche parmi les enfants du nœud courant une action identique ;
      - si trouvée, avance à cet enfant et renvoie son observation ;
      - sinon, renvoie [NON SIMULÉ] sans bouger.
    """

    def __init__(self, tree: SearchTree, start_node_id: int) -> None:
        self.tree = tree
        self.start_node_id = start_node_id
        self.current_id = start_node_id

    def reset(self) -> None:
        self.current_id = self.start_node_id

    def step(self, action: Action) -> Observation:
        for child in self.tree.children(self.current_id):
            if child.action is not None and child.action.key() == action.key():
                self.current_id = child.id
                obs = child.observation or Observation(output="")
                # On marque l'observation comme simulée (rejouée).
                return Observation(
                    output=obs.output,
                    exit_code=obs.exit_code,
                    truncated=obs.truncated,
                    simulated=True,
                    unsimulated=False,
                )
        return Observation(output="[NON SIMULÉ]", simulated=True, unsimulated=True)

    # Utilitaire pour le rêveur : où en est-on dans l'arbre ?
    def position(self) -> Node | None:
        return self.tree.get_node(self.current_id)


class MemorySimulator(World):
    """Monde de rêve à mémoire globale : toute action déjà jouée dans la
    tentative, quelle que soit sa position dans l'arbre, renvoie l'observation
    enregistrée. Permet au rêve de « sauter » des étapes et donc de découvrir
    des raccourcis. Une action jamais jouée renvoie [NON SIMULÉ].

    Global-memory dream world: any action already played in the attempt
    (anywhere in the tree) returns its recorded observation.
    """

    def __init__(self, tree: SearchTree, attempt_id: str) -> None:
        self.memory: dict[str, Observation] = {}
        for node in tree.attempt_nodes(attempt_id):
            # Meta tools have no real output to replay
            if node.action is None or node.observation is None:
                continue
            if node.action.tool in ("set_hypothesis", "submit_flag", "create_tool"):
                continue
            self.memory.setdefault(norm_key(node.action), node.observation)

    def reset(self) -> None:
        pass  # stateless: the memory never changes during a dream

    def step(self, action: Action) -> Observation:
        obs = self.memory.get(norm_key(action))
        if obs is None:
            return Observation(output="[NON SIMULÉ]", simulated=True, unsimulated=True)
        return Observation(output=obs.output, exit_code=obs.exit_code,
                           truncated=obs.truncated, simulated=True)


def norm_key(action: Action) -> str:
    """Clé d'action tolérante : espaces multiples et préfixes './' ignorés,
    pour que `strings  ./x` et `strings x` soient reconnues comme identiques.
    Lenient action key (extra spaces and './' prefixes ignored).
    """
    import json
    import re

    def clean(v):
        if isinstance(v, str):
            v = re.sub(r"\s+", " ", v.strip())
            return re.sub(r"(^|\s)\./", r"\1", v)
        return v

    args = {k: clean(v) for k, v in action.args.items()}
    return action.tool + "::" + json.dumps(args, sort_keys=True, ensure_ascii=False)

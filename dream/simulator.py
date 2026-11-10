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

"""Arbre de recherche ⑥ — mémoire des tentatives, sur SQLite.

Chaque action de l'agent crée un nœud (hypothèse, action, observation). Le
chemin qui mène au flag est marqué `on_solution_path`. La phase de rêve relit
cet arbre pour rejouer les mauvaises bifurcations ; le simulateur ⑦ s'appuie sur
les observations enregistrées.

Base par défaut : `data/trees.db` (créée à la demande).
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterator

from core.types import Action, Attempt, Node, Observation

_SCHEMA = """
CREATE TABLE IF NOT EXISTS attempts (
    id            TEXT PRIMARY KEY,
    challenge     TEXT NOT NULL,
    policy        TEXT NOT NULL,
    solved        INTEGER NOT NULL DEFAULT 0,
    flag          TEXT,
    steps         INTEGER NOT NULL DEFAULT 0,
    root_id       INTEGER,
    solution_leaf INTEGER,
    ts            REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS nodes (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id    TEXT NOT NULL,
    parent_id     INTEGER,
    depth         INTEGER NOT NULL DEFAULT 0,
    hypothesis    TEXT,
    action_json   TEXT,
    obs_json      TEXT,
    on_sol_path   INTEGER NOT NULL DEFAULT 0,
    ts            REAL NOT NULL,
    FOREIGN KEY (attempt_id) REFERENCES attempts(id)
);
CREATE INDEX IF NOT EXISTS idx_nodes_attempt ON nodes(attempt_id);
CREATE INDEX IF NOT EXISTS idx_nodes_parent  ON nodes(parent_id);
"""


class SearchTree:
    """Accès à l'arbre de recherche persistant."""

    def __init__(self, db_path: str | Path = "data/trees.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(_SCHEMA)
        self.conn.commit()

    # -- écriture --------------------------------------------------------- #
    def start_attempt(self, attempt: Attempt) -> int:
        """Enregistre une tentative et crée son nœud racine. Renvoie l'id racine."""
        import time

        self.conn.execute(
            "INSERT OR REPLACE INTO attempts "
            "(id, challenge, policy, solved, flag, steps, root_id, solution_leaf, ts) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (attempt.id, attempt.challenge_name, attempt.policy_version,
             int(attempt.solved), attempt.flag, attempt.steps,
             None, None, time.time()),
        )
        cur = self.conn.execute(
            "INSERT INTO nodes (attempt_id, parent_id, depth, hypothesis, "
            "action_json, obs_json, on_sol_path, ts) VALUES (?,?,?,?,?,?,?,?)",
            (attempt.id, None, 0, None, None, None, 0, time.time()),
        )
        root_id = int(cur.lastrowid)
        self.conn.execute("UPDATE attempts SET root_id=? WHERE id=?", (root_id, attempt.id))
        self.conn.commit()
        return root_id

    def add_node(
        self,
        attempt_id: str,
        parent_id: int,
        action: Action,
        observation: Observation,
        *,
        hypothesis: str | None = None,
    ) -> int:
        """Ajoute un nœud enfant et renvoie son id."""
        import time

        parent = self.get_node(parent_id)
        depth = (parent.depth + 1) if parent else 1
        cur = self.conn.execute(
            "INSERT INTO nodes (attempt_id, parent_id, depth, hypothesis, "
            "action_json, obs_json, on_sol_path, ts) VALUES (?,?,?,?,?,?,?,?)",
            (
                attempt_id,
                parent_id,
                depth,
                hypothesis or action.hypothesis,
                json.dumps({"tool": action.tool, "args": action.args}, ensure_ascii=False),
                json.dumps(
                    {
                        "output": observation.output,
                        "exit_code": observation.exit_code,
                        "truncated": observation.truncated,
                        "simulated": observation.simulated,
                        "unsimulated": observation.unsimulated,
                    },
                    ensure_ascii=False,
                ),
                0,
                time.time(),
            ),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def mark_solution_path(self, attempt_id: str, leaf_id: int, flag: str, steps: int) -> None:
        """Marque la branche gagnante et clôt la tentative."""
        node_id: int | None = leaf_id
        while node_id is not None:
            self.conn.execute("UPDATE nodes SET on_sol_path=1 WHERE id=?", (node_id,))
            row = self.conn.execute(
                "SELECT parent_id FROM nodes WHERE id=?", (node_id,)
            ).fetchone()
            node_id = row["parent_id"] if row else None
        self.conn.execute(
            "UPDATE attempts SET solved=1, flag=?, steps=?, solution_leaf=? WHERE id=?",
            (flag, steps, leaf_id, attempt_id),
        )
        self.conn.commit()

    # -- lecture ---------------------------------------------------------- #
    def get_node(self, node_id: int) -> Node | None:
        row = self.conn.execute("SELECT * FROM nodes WHERE id=?", (node_id,)).fetchone()
        return _row_to_node(row) if row else None

    def children(self, node_id: int) -> list[Node]:
        rows = self.conn.execute(
            "SELECT * FROM nodes WHERE parent_id=? ORDER BY id", (node_id,)
        ).fetchall()
        return [_row_to_node(r) for r in rows]

    def attempt_nodes(self, attempt_id: str) -> list[Node]:
        rows = self.conn.execute(
            "SELECT * FROM nodes WHERE attempt_id=? ORDER BY id", (attempt_id,)
        ).fetchall()
        return [_row_to_node(r) for r in rows]

    def solved_attempts(self) -> Iterator[Attempt]:
        rows = self.conn.execute("SELECT * FROM attempts WHERE solved=1").fetchall()
        for r in rows:
            yield _row_to_attempt(r)

    def bad_forks(self, attempt_id: str) -> list[Node]:
        """Nœuds hors du chemin gagnant dont le parent, lui, est sur le chemin.

        Ce sont les « mauvaises bifurcations » que le rêve rejoue : à partir
        d'un bon état, l'agent avait pris une direction qui n'aboutit pas.
        """
        rows = self.conn.execute(
            "SELECT n.* FROM nodes n JOIN nodes p ON n.parent_id = p.id "
            "WHERE n.attempt_id=? AND n.on_sol_path=0 AND p.on_sol_path=1 "
            "ORDER BY n.id",
            (attempt_id,),
        ).fetchall()
        return [_row_to_node(r) for r in rows]

    def path_to_root(self, node_id: int) -> list[Node]:
        """Chemin racine → nœud (ordre racine d'abord)."""
        chain: list[Node] = []
        cur: int | None = node_id
        while cur is not None:
            node = self.get_node(cur)
            if node is None:
                break
            chain.append(node)
            cur = node.parent_id
        return list(reversed(chain))

    def close(self) -> None:
        self.conn.close()


def _row_to_node(row: sqlite3.Row) -> Node:
    action = None
    if row["action_json"]:
        d = json.loads(row["action_json"])
        action = Action(tool=d.get("tool", ""), args=d.get("args", {}),
                        hypothesis=row["hypothesis"])
    obs = None
    if row["obs_json"]:
        o = json.loads(row["obs_json"])
        obs = Observation(
            output=o.get("output", ""),
            exit_code=o.get("exit_code"),
            truncated=o.get("truncated", False),
            simulated=o.get("simulated", False),
            unsimulated=o.get("unsimulated", False),
        )
    return Node(
        id=row["id"],
        parent_id=row["parent_id"],
        attempt_id=row["attempt_id"],
        action=action,
        observation=obs,
        depth=row["depth"],
        hypothesis=row["hypothesis"],
        on_solution_path=bool(row["on_sol_path"]),
        ts=row["ts"],
    )


def _row_to_attempt(row: sqlite3.Row) -> Attempt:
    return Attempt(
        id=row["id"],
        challenge_name=row["challenge"],
        policy_version=row["policy"],
        solved=bool(row["solved"]),
        flag=row["flag"],
        steps=row["steps"],
        root_id=row["root_id"],
        solution_leaf_id=row["solution_leaf"],
    )

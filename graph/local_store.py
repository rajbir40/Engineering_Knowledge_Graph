import os
import pickle
import networkx as nx
from graph.storage import GraphStorage


class LocalGraphStore(GraphStorage):

    def __init__(self, path="graph.db"):
        self.path = path
        self.graph = nx.DiGraph()
        self._load()

    # ---------- Persistence ----------
    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as f:
                self.graph = pickle.load(f)

    def _save(self):
        with open(self.path, "wb") as f:
            pickle.dump(self.graph, f)

    # ---------- Node Ops ----------
    def upsert_node(self, node: dict):
        self.graph.add_node(
            node["id"],
            type=node["type"],
            name=node["name"],
            **node.get("properties", {})
        )
        self._save()

    def get_node(self, node_id: str):
        if node_id not in self.graph:
            return None
        return self.graph.nodes[node_id]

    def get_nodes_by_type(self, node_type: str):
        return [
            (n, d)
            for n, d in self.graph.nodes(data=True)
            if d.get("type") == node_type
        ]

    def delete_node(self, node_id: str):
        if node_id in self.graph:
            self.graph.remove_node(node_id)
            self._save()

    # ---------- Edge Ops ----------
    def upsert_edge(self, edge: dict):
        self.graph.add_edge(
            edge["source"],
            edge["target"],
            type=edge["type"],
            **edge.get("properties", {})
        )
        self._save()

    def get_graph(self):
        return self.graph


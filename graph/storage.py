from abc import ABC, abstractmethod

class GraphStorage(ABC):

    @abstractmethod
    def upsert_node(self, node: dict):
        pass

    @abstractmethod
    def upsert_edge(self, edge: dict):
        pass

    @abstractmethod
    def get_node(self, node_id: str):
        pass

    @abstractmethod
    def get_nodes_by_type(self, node_type: str):
        pass

    @abstractmethod
    def delete_node(self, node_id: str):
        pass

    @abstractmethod
    def get_graph(self):
        pass

    def out_edges(self, node_id):
        if node_id not in self.graph:
            return []
        return self.graph.out_edges(node_id, data=True)

    def in_edges(self, node_id):
        if node_id not in self.graph:
            return []
        return self.graph.in_edges(node_id, data=True)
    
    def add_node(self, node):
        pass

    def add_edge(self, edge):
        pass
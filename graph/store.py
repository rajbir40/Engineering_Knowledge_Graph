class GraphStore:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node):
        self.nodes[node["id"]] = node   

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_node(self, node_id):
        return self.nodes.get(node_id)

    def summary(self):
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges)
        }
    
    def print_graph(self):
        print("\n===== NODES =====")
        for node_id, node in self.nodes.items():
            print(f"{node_id} -> {node}")

        print("\n===== EDGES =====")
        for edge in self.edges:
            print(f'{edge["source"]} -[{edge["type"]}]-> {edge["target"]}')

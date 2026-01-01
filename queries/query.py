import networkx as nx

class QueryEngine:
    def __init__(self, graph_store):
        self.store = graph_store
        self.graph = graph_store.get_graph()

    def get_node(self, node_id):
        if node_id not in self.graph:
            return None
        return {
            "id": node_id,
            **self.graph.nodes[node_id]
        }

    def get_nodes(self, node_type):
        results = []
        for node_id, data in self.graph.nodes(data=True):
            if data.get("type") == node_type:
                results.append({
                    "id": node_id,
                    **data
                })
        return results

    def downstream(self, node_id):
        visited = set()
        result = set()

        def dfs(n):
            for _, target, data in self.graph.out_edges(n, data=True):
                if target not in visited:
                    visited.add(target)
                    result.add(target)
                    dfs(target)

        dfs(node_id)
        return list(result)

    def upstream(self, node_id):
        visited = set()
        result = set()

        def dfs(n):
            for source, _, data in self.graph.in_edges(n, data=True):
                if source not in visited:
                    visited.add(source)
                    result.add(source)
                    dfs(source)

        dfs(node_id)
        return list(result)

    def blast_radius(self, node_id):
        impacted = set()
        impacted.add(node_id)

        upstream_nodes = self.upstream(node_id)
        downstream_nodes = self.downstream(node_id)

        impacted.update(upstream_nodes)
        impacted.update(downstream_nodes)

        teams = set()
        for n in impacted:
            owner = self.get_owner(n)
            if owner:
                teams.add(owner)

        return {
            "nodes": list(impacted),
            "teams": list(teams)
        }


    def path(self, from_id, to_id):
        try:
            return nx.shortest_path(self.graph, from_id, to_id)
        except nx.NetworkXNoPath:
            return None

    def get_owner(self, node_id):
        for _, target, data in self.graph.out_edges(node_id, data=True):
            if data.get("type") == "owns":
                return target
        return None



def make_node(node_type, name, properties=None):
    return {
        "id": f"{node_type}:{name}",
        "type": node_type,
        "name": name,
        "properties": properties or {}
    }


def make_edge(edge_type, source, target, properties=None):
    return {
        "id": f"edge:{source}-to-{target}-{edge_type}",
        "type": edge_type,
        "source": source,
        "target": target,
        "properties": properties or {}
    }

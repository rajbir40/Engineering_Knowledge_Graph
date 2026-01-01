def execute_intent(intent: dict, graph_store):
    G = graph_store.graph  # 👈 actual NetworkX graph

    intent_type = intent["intent"]
    entity = intent["entity_name"]
    entity_type = intent["entity_type"]

    node_id = f"{entity_type}:{entity}"

    # ---------- OWNERSHIP ----------
    if intent_type == "ownership":
        if node_id not in G:
            return f"I don't know about {entity}"

        for src, _, data in G.in_edges(node_id, data=True):
            if data.get("type") == "owns":
                return f"{entity} is owned by {src.split(':')[1]}"

        return f"No ownership info found for {entity}"


    # ---------- LIST ----------
    if intent_type == "list":
        nodes = graph_store.get_nodes_by_type(entity_type)
        names = [n.split(":")[1] for n, _ in nodes]
        return ", ".join(names)

    # ---------- BLAST RADIUS ----------
    if intent_type == "blast_radius":
        impacted = set()
        for src, _ in G.in_edges(node_id):
            impacted.add(src.split(":")[1])

        if not impacted:
            return f"No services depend on {entity}"

        return f"If {entity} goes down, impacted services: {', '.join(impacted)}"

    return "Sorry, I couldn't understand that."

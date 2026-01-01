CONNECTORS = []

def register(connector_cls):
    """
    Decorator to auto-register connectors
    """
    CONNECTORS.append(connector_cls())
    return connector_cls


def run_all_connectors(graph):
    for connector in CONNECTORS:
        print(f"🔌 Running connector: {connector.name()}")
        connector.parse(graph)

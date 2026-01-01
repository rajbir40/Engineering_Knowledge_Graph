from graph.local_store import LocalGraphStore
from connectors.registry import run_all_connectors
from cli import start_cli


def main():
    graph = LocalGraphStore()

    run_all_connectors(graph)

    start_cli()


if __name__ == "__main__":
    main()
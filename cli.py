from chat.intent_parser import parse_intent
from chat.executor import execute_intent
from graph.local_store import LocalGraphStore


def start_cli():
    graph = LocalGraphStore()

    print("Engineering Knowledge Graph Chat")
    print("Type 'exit' to quit\n")

    while True:
        try:
            user_input = input("> ").strip()
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye ")
                break

            intent = parse_intent(user_input)
            response = execute_intent(intent, graph)
            print(response)

        except KeyboardInterrupt:
            print("\nExiting...")
            break

        except Exception as e:
            print("Error:", str(e))


if __name__ == "__main__":
    start_cli()

import yaml
from graph.models import make_node, make_edge


def parse_teams(path, graph):
    with open(path) as f:
        data = yaml.safe_load(f)

    for team in data.get("teams", []):
        team_name = team["name"]

        team_node = make_node(
            "team",
            team_name,
            {
                "lead": team.get("lead"),
                "slack": team.get("slack_channel"),
                "pagerduty": team.get("pagerduty_schedule")
            }
        )
        graph.upsert_node(team_node)

        for owned in team.get("owns", []):
            for node_type in ["service", "database", "cache"]:
                node_id = f"{node_type}:{owned}"
                if graph.get_node(node_id):
                    graph.upsert_edge(
                        make_edge(
                            "owns",
                            f"team:{team_name}",
                            node_id
                        )
                    )

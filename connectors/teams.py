import yaml
from connectors.base import BaseConnector
from connectors.registry import register
from graph.models import make_node, make_edge


@register
class TeamsConnector(BaseConnector):

    def name(self):
        return "teams"

    def parse(self, graph):
        with open("data/teams.yaml") as f:
            data = yaml.safe_load(f)

        for team in data.get("teams", []):
            team_node = make_node(
                "team",
                team["name"],
                {
                    "lead": team.get("lead"),
                    "slack": team.get("slack_channel"),
                    "pagerduty": team.get("pagerduty_schedule")
                }
            )
            graph.upsert_node(team_node)

            for owned in team.get("owns", []):
                graph.upsert_edge(
                    make_edge(
                        "owns",
                        f"team:{team['name']}",
                        f"service:{owned}"
                    )
                )

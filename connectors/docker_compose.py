import yaml
from connectors.base import BaseConnector
from connectors.registry import register
from graph.models import make_node, make_edge


@register
class DockerComposeConnector(BaseConnector):

    def name(self):
        return "docker-compose"

    def parse(self, graph):
        with open("data/docker_compose.yml") as f:
            compose = yaml.safe_load(f)

        services = compose.get("services", {})

        for service_name, config in services.items():
            labels = config.get("labels", {})
            env_vars = config.get("environment", [])
            depends_on = config.get("depends_on", [])

            service_node = make_node(
                "service",
                service_name,
                {
                    "team": labels.get("team"),
                    "oncall": labels.get("oncall"),
                    "pci_compliant": labels.get("pci_compliant")
                }
            )
            graph.upsert_node(service_node)

            # depends_on → calls
            for dep in depends_on:
                graph.upsert_edge(
                    make_edge(
                        "calls",
                        f"service:{service_name}",
                        f"service:{dep}"
                    )
                )

            # env-based deps
            for env in env_vars:
                if "DATABASE_URL" in env:
                    db = env.split("@")[-1].split(":")[0]
                    graph.upsert_node(make_node("database", db))
                    graph.upsert_edge(
                        make_edge(
                            "reads_from",
                            f"service:{service_name}",
                            f"database:{db}"
                        )
                    )

                if "REDIS_URL" in env:
                    cache = env.split("//")[-1].split(":")[0]
                    graph.upsert_node(make_node("cache", cache))
                    graph.upsert_edge(
                        make_edge(
                            "uses",
                            f"service:{service_name}",
                            f"cache:{cache}"
                        )
                    )

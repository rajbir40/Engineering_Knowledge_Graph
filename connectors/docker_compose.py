import yaml
from graph.models import make_node, make_edge


def parse_docker_compose(path, graph):
    with open(path) as f:
        compose = yaml.safe_load(f)

    services = compose.get("services", {})

    for service_name, config in services.items():
        labels = config.get("labels", {})
        env_vars = config.get("environment", [])
        depends_on = config.get("depends_on", [])

        # SERVICE NODE
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

        #  DEPENDS_ON (SERVICE → SERVICE)
        for dep in depends_on:
            edge = make_edge(
                "calls",
                f"service:{service_name}",
                f"service:{dep}"
            )
            graph.upsert_edge(edge)

        # ENV BASED DEPENDENCIES 
        for env in env_vars:
            if "DATABASE_URL" in env:
                db_name = extract_db_name(env)
                db_node = make_node("database", db_name)
                graph.upsert_node(db_node)

                graph.upsert_edge(
                    make_edge(
                        "reads_from",
                        f"service:{service_name}",
                        f"database:{db_name}"
                    )
                )

            if "REDIS_URL" in env:
                cache_name = extract_cache_name(env)
                cache_node = make_node("cache", cache_name)
                graph.upsert_node(cache_node)

                graph.upsert_edge(
                    make_edge(
                        "uses",
                        f"service:{service_name}",
                        f"cache:{cache_name}"
                    )
                )

        #  DATABASE / CACHE SERVICES 
        if labels.get("type") == "database":
            db_node = make_node(
                "database",
                service_name,
                {"team": labels.get("team")}
            )
            graph.upsert_node(db_node)

        if labels.get("type") == "cache":
            cache_node = make_node(
                "cache",
                service_name,
                {"team": labels.get("team")}
            )
            graph.upsert_node(cache_node)


def extract_db_name(env):
    # postgresql://...@payments-db:5432/payments
    return env.split("@")[-1].split(":")[0]


def extract_cache_name(env):
    # redis://redis-main:6379
    return env.split("//")[-1].split(":")[0]

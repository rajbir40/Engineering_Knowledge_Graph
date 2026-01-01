from graph.local_store import LocalGraphStore
from connectors.docker_compose import parse_docker_compose
from connectors.teams import parse_teams

graph = LocalGraphStore()

parse_docker_compose("data/docker_compose.yml", graph)
parse_teams("data/teams.yaml", graph)

print("Graph loaded successfully")

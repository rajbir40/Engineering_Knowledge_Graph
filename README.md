# Engineering Knowledge Graph (EKG)

This project is a prototype **Engineering Knowledge Graph** that parses real-world infrastructure configuration files, builds a unified graph of services, databases, caches, and teams, and allows querying this graph using **natural language** through a chat interface.

The goal of this project is to demonstrate how engineering metadata scattered across config files can be connected, queried, and reasoned about in a structured way.

---

## A. Setup & Usage

### Prerequisites

- Docker & Docker Compose installed
- Ollama installed on the host machine (used for local LLM inference)
- No local Python setup required (everything runs inside Docker)

---

### Startup Instructions (Detached Mode)

Run the following commands **in order**:

```bash
# Start Ollama service
docker compose up -d ollama

# Pull the LLM model once
docker compose exec ollama ollama pull llama3

# Build the application image
docker compose up --build
````

This will:

* Parse configuration files
* Build the knowledge graph

---

### Start the Chat Interface

Open a **new terminal**:

```bash
docker compose up -d
docker compose exec ekg python app.py
```

You should see:

```text
🧠 Engineering Knowledge Graph Chat
Type 'exit' to quit
>
```

---

### Example Queries

```text
Who owns the payment service?
What breaks if redis-main goes down?
What's the blast radius of users-db?
```

---

### Environment Variables

No external API keys are required.

* LLM runs locally via **Ollama**
* Model used: `llama3`

---

## B. Architecture Overview

### High-Level Data Flow

```
Config Files
(docker-compose.yml, teams.yaml, k8s)
        ↓
     Connectors
        ↓
  Graph Storage Layer
        ↓
   Query Engine
        ↓
  Natural Language Chat
```

---

### Key Components

**Connectors (`connectors/`)**

* Parse raw configuration files
* Emit normalized nodes and edges
* Designed to be pluggable and independent

**Graph Storage (`graph/`)**

* Directed graph implementation
* Supports upsert, lookup, deletion, traversal
* Persists graph to disk so data survives restarts

**Query Engine (`graph/query.py`)**

* Handles ownership, dependency, blast-radius, and path queries
* Traversal logic is deterministic and cycle-safe

**Chat Interface (`cli.py`, `chat/`)**

* CLI-based interface
* Uses LLM only for intent extraction
* Executes graph queries deterministically

---

## C. Design Questions

### 1. Connector pluggability

Each connector follows the same pattern: it accepts a file path and a graph store instance, then emits nodes and edges.
To add a new connector (for example, Terraform), a developer only needs to create a new file in the `connectors/` directory and register it at startup.
No changes are required in the graph storage or chat logic.

---

### 2. Graph updates

The graph is rebuilt on startup by re-running all connectors.
Nodes and edges are **upserted**, ensuring the latest configuration state is reflected.
This avoids stale data while keeping the implementation simple and predictable.

---

### 3. Cycle handling

All graph traversals maintain a `visited` set.
This prevents infinite loops even if cyclic dependencies exist between services.
Traversal depth is controlled explicitly in query functions.

---

### 4. Query mapping

Natural language input is first converted into a structured intent using an LLM.
The intent is then mapped to predefined graph operations such as ownership lookup or blast-radius analysis.
This separation ensures correctness and avoids hallucinated answers.

---

### 5. Failure handling

If a query cannot be parsed or required graph data is missing, the system responds with a safe fallback message.
The LLM never fabricates answers — it only identifies intent.
All final responses are generated from actual graph data.

---

### 6. Scale considerations

At around 10K nodes, in-memory traversal and pickle-based persistence would start to degrade.
The first bottlenecks would be graph traversal performance and disk I/O.
At that point, migrating to Neo4j or a managed graph database would be necessary.

---

### 7. GraphDB choice

This implementation uses **NetworkX with disk persistence** instead of Neo4j.
The reason is simplicity, ease of debugging, and zero external dependencies for a prototype.
Neo4j would be the preferred choice for production due to indexing, Cypher queries, and better scalability.

---

## D. Tradeoffs & Limitations

* A CLI was used instead of a web UI to focus on core functionality
* Intent parsing is intentionally minimal and conservative
* Graph updates happen only on startup (no live file watching)

**Weakest part:**
Some natural language queries still fail or require rephrasing.

**With 20 more hours, I would:**

* Improve intent parsing coverage for edge cases
* Add support for more query patterns
* Introduce Neo4j as a backend
* Build a simple web UI
* Add graph visualization for dependency paths

---

## E. AI Usage

AI helped significantly with:

* Designing intent schemas
* Structuring query patterns
* Speeding up implementation of repetitive logic

Some AI-generated suggestions were intentionally rejected when they added unnecessary complexity or reduced clarity.
Several parts of the implementation required manual correction and simplification.

The biggest learning was that AI is most effective when used as a **helper**, not as the decision-maker.

---

## Demo Video

**Demo Walkthrough (3–5 minutes):**
Google Drive (Unlisted):
**[https://drive.google.com/file/d/XXXXXXXXXXXX/view](https://drive.google.com/file/d/1VY9sBxXm9vBDhrxE8MfZcP93jxaZaIyx/view?usp=drive_link)**

The video demonstrates:

* System startup using Docker
* Connectors parsing configuration files
* Natural language queries
* Blast radius analysis

Separation of LLM and Execution (Design Decision):

* The LLM in this system is used only to understand the user’s intent, not to access data or execute graph queries.
Once the intent is extracted, all logic such as traversing dependencies, finding owners, or calculating blast radius is handled by deterministic Python code.

* This separation helps prevent hallucination because the LLM never generates answers on its own.
It also makes the system easier to debug, since graph behavior is predictable and not dependent on model output.
Overall, this keeps the system reliable while still benefiting from natural language input.
---

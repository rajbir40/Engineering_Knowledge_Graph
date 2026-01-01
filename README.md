# Engineering Knowledge Graph (EKG)

A prototype system that parses engineering configuration files (Docker Compose, team metadata, optional Kubernetes manifests), builds a unified **Engineering Knowledge Graph**, and provides a **natural-language chat interface** to query ownership, dependencies, and blast radius.

---

## A. Setup & Usage

### Prerequisites

* Docker & Docker Compose installed
* Ollama installed on host (for local LLM inference)
* Python is **not required locally** (runs inside Docker)

---

### Startup Instructions (Detached Mode)

Run the following commands **in order**:

```bash
# Start Ollama service
docker compose up -d ollama

# Pull the LLM model once
docker compose exec ollama ollama pull llama3

# Build application image
docker compose up --build

```

The system now:

* Parses configuration files
* Builds the knowledge graph
* Starts the chat interface inside the container

---

### Start the Chat Interface

Open a new terminal:

```bash
docker compose up -d
docker compose exec ekg python app.py
```

You will see:

```
🧠 Engineering Knowledge Graph Chat
Type 'exit' to quit
>
```

---

### Example Queries You Can Ask

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
   Query Executor
        ↓
  Natural Language Chat
```

---

### Key Components

* **Connectors (`connectors/`)**

  * Parse raw config files
  * Emit normalized nodes & edges
  * Designed to be pluggable

* **Graph Storage (`graph/`)**

  * Stores nodes & edges using a directed graph
  * Persists graph to disk
  * Supports upsert, lookup, traversal

* **Query Engine (`chat/executor.py`)**

  * Executes ownership, dependency, blast-radius queries

* **Chat Interface (`cli.py`)**

  * CLI-based interface
  * Uses LLM for intent parsing
  * Maintains simple conversation context

---

## C. Design Questions

### 1. Connector pluggability

Connectors follow a common interface: they accept a file path and a graph store instance, and emit nodes and edges.
To add a new connector (e.g., Terraform), a developer only needs to add a new file in `connectors/` and register it during startup.
No changes to the graph core or chat layer are required.

---

### 2. Graph updates

On startup, connectors re-parse the source configuration files and **upsert** nodes and edges.
This ensures the graph always reflects the latest state of config files.
Stale nodes can optionally be cleaned by tracking file provenance.

---

### 3. Cycle handling

All traversal operations use **visited sets** to track already-seen nodes.
This prevents infinite loops even if the graph contains cycles.
NetworkX inherently supports safe traversal patterns.

---

### 4. Query mapping

Natural language is first translated into a **structured intent JSON** using an LLM.
The system then maps intent types (ownership, blast_radius, list, etc.) to deterministic graph operations.
This keeps the LLM out of execution logic and prevents hallucination.

---

### 5. Failure handling

If intent parsing fails or the graph lacks required data, the system returns a clarification or “not found” response.
The LLM is never allowed to fabricate graph answers.
This ensures correctness over fluency.

---

### 6. Scale considerations

At ~10K nodes, in-memory traversal and pickle-based persistence would become slow.
The first bottleneck would be graph traversal performance and persistence.
At scale, migrating to Neo4j or a managed graph DB would be required.

---

### 7. GraphDB choice

This implementation uses a **local persisted graph (NetworkX + pickle)** instead of Neo4j.
Reason: simplicity, zero external dependencies, and fast prototyping.
Neo4j would be preferred for production due to Cypher queries, indexing, and scalability.

---

## D. Tradeoffs & Limitations

* Skipped a web UI in favor of CLI to focus on core logic
* Simplified intent parsing to a small intent schema
* No real-time file watching; graph updates occur on startup

**Weakest part:**
LLM intent parsing can fail on very ambiguous queries.

**With 20 more hours, I would:**

* Add Neo4j backend
* Implement graph diffing & incremental updates
* Build a web-based chat UI
* Add visualization of graph paths

---

## E. AI Usage

* AI helped most with **intent parsing logic** and query phrasing
* Several AI-generated suggestions were rejected due to over-engineering
* Learned that AI works best when constrained to **small, well-defined roles**
* Deterministic graph logic must remain non-AI

---

## Demo Video Checklist (3–5 Minutes)

When recording:

1. Show `docker compose up -d`
2. Explain connectors parsing files
3. Show graph building (print summary)
4. Run **5+ queries**, including:

   * Ownership
   * Blast radius
   * Listing entities
5. Explain one design decision (pluggable connectors or LLM separation)

---

## Final Note

This project demonstrates:

* Systems thinking
* Graph modeling
* Safe AI integration
* Production-aware design tradeoffs

---

## Version 3 Proposal: Dedicated Vector Storage Service

### Objective

Separate the FAISS vector index from the Core Engine by deploying it as an independent service. This allows the orchestration engine and vector database to scale independently while improving memory efficiency.

---

### Current Limitation

In large enterprise deployments, the vector database may contain millions of embeddings.

When FAISS is embedded directly within the Core Engine:

* Memory usage increases as the index grows.
* Large indexes consume significant RAM and increase the risk of out-of-memory (OOM) failures.
* Every additional Core Engine replica duplicates the entire vector index, resulting in unnecessary memory consumption and inefficient horizontal scaling.

---

### Proposed Architecture

The Core Engine treats vector search as an external service rather than an in-process library.

```text
Core Engine
      │
      ▼
Vector Storage Service (FAISS)
      │
      ▼
Persistent Vector Index
```

The Vector Storage Service maintains the FAISS index and processes similarity search requests, while the Core Engine communicates with it through HTTP or gRPC.

---

### Benefits

* **Independent Scaling** – The Core Engine and vector service can scale separately.
* **Reduced Memory Usage** – Executor instances no longer load large vector indexes into memory.
* **Persistent Storage** – Vector indexes remain available across container restarts.
* **Flexible Infrastructure** – Memory-intensive vector storage can be deployed on high-memory nodes, while the Core Engine runs on standard compute nodes.

---

### Implementation

1. Wrap FAISS inside a lightweight FastAPI or gRPC service.
2. Store the FAISS index on a persistent Docker volume.
3. Configure the Core Engine to perform vector search through the dedicated service instead of accessing FAISS directly.

---

### Expected Outcome

By externalizing vector storage, the Core Engine becomes a lightweight, stateless service that scales efficiently, while the Vector Storage Service independently manages large embedding indexes and memory-intensive similarity search operations. This architecture improves scalability, resource utilization, and maintainability for enterprise-scale deployments.

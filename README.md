
---

# 🚀 Orion

**Orion** is an MCP-based dynamic retrieval system that uses LLM-driven orchestration to execute intelligent search strategies across multiple tools.

Instead of a fixed pipeline, Orion builds and executes **dynamic retrieval DAGs** using the Model Context Protocol (MCP), enabling adaptive querying over structured, semantic, and real-time data sources.

The system supports:

* Vector search (semantic retrieval)
* Structured database filtering
* Metadata-based refinement
* Web search integration

All tools are orchestrated through a central MCP execution layer that plans, executes, and aggregates results into a final response.

---

## 📌 Architecture Overview

Orion follows a graph-based execution model:

```
User Query → MCP Planner → DAG Execution → Tool Layer → Context → Final LLM Answer
```

---

## 📂 More Details

Full system design, tool specifications, and deployment architecture are available in the `/docs` directory.

---

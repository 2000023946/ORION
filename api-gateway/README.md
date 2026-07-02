
---

# MCP Dynamic Retrieval System

## Overview

This project implements a **dynamic retrieval pipeline using MCP (Model Context Protocol)** where an LLM does not directly answer questions, but instead:

1. **Plans execution (DAG generation)**
2. **Executes tools via MCP server**
3. **Builds context from tool outputs**
4. **Generates final answer using LLM with retrieved context**

This allows **adaptive multi-tool reasoning instead of fixed pipelines**.

---

## Core Idea

```
User Query
   ↓
LLM Planner (creates DAG)
   ↓
Graph Executor (runs DAG)
   ↓
MCP Server (executes tools)
   ↓
Tool Outputs → Context
   ↓
Final LLM Answer
```

---

## Key Design Philosophy

* Everything is **interface-driven (ports & adapters)**
* Tools are **independent MCP nodes**
* Execution is **graph-based (DAG, not pipeline)**
* Retrieval is **dynamic (not fixed order)**
* System is designed to scale to **multi-machine execution later**

---

## System Components

### 1. MCP Client (Planner + Answer LLM)

Responsible for:

* Converting user query → execution DAG
* Generating final answer from context

Files:

* `src/infrastructure/real/mcp_client/`

---

### 2. MCP Server (Tool Runtime)

Responsible for:

* Registering tools
* Executing tools via `call_tool`
* Returning structured outputs

Files:

* `src/infrastructure/real/mcp_server/`

---

### 3. Graph Executor

Responsible for:

* Executing DAG layer-by-layer
* Managing tool dependencies
* Passing outputs between tools
* Building execution context

File:

* `src/infrastructure/real/graph_executor/real_graph_executor.py`

---

### 4. Tools (MCP Nodes)

You currently support 4 tools:

* **VECTOR_SEARCH_TOOL**

  * Input: query
  * Output: doc_ids
  * Semantic search over embeddings

* **WEB_SEARCH_TOOL**

  * Input: query
  * Output: web results
  * Live external search

* **DB_FILTER_TOOL**

  * Input: query
  * Output: filtered documents
  * Structured filtering (name + price)

* **METADATA_FILTER_TOOL**

  * Input: doc_ids
  * Output: documents
  * Filters vector search results using metadata constraints

---

## Execution Model (IMPORTANT)

### Step 1 — Planning (LLM)

The LLM generates a DAG like:

```json
{
  "edges": [
    ["START", "VECTOR_SEARCH_TOOL"],
    ["START", "WEB_SEARCH_TOOL"],
    ["VECTOR_SEARCH_TOOL", "METADATA_FILTER_TOOL"],
    ["DB_FILTER_TOOL", "END"],
    ["WEB_SEARCH_TOOL", "END"],
    ["METADATA_FILTER_TOOL", "END"]
  ]
}
```

---

### Step 2 — Graph Execution

The executor:

* Runs all tools at same depth in parallel
* Passes outputs via registry
* Resolves dependencies using edges
* Stops at END node

---

### Step 3 — Context Building

All tool outputs are stored in:

```
Context
```

Example:

* vector search → doc_ids
* metadata filter → documents
* web search → results

---

### Step 4 — Final Answer LLM

The MCP client sends:

```
Query + Context → LLM → Final Answer
```

---

## Important Rules in System

### DAG Rules

* Must be **acyclic**
* Must follow **strict IO matching**
* No hallucinated tool dependencies
* START = query input
* END = completion

---

### Tool Rules

* Tools only run if required inputs exist
* No tool can "guess" missing inputs
* Metadata filter requires doc_ids
* DB filter requires query
* Vector search always produces doc_ids

---

## Local Setup

### Requirements

* Python 3.10+
* Docker Daemon & Docker terminal or MongoDB (Need for DB to have running mongoDB running)

---

### Install

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Run Tests

Each component has isolated tests:

#### Tool Tests

```bash
python test.tool.vector_search.py
python test.tool.web_search.py
python test.tool.db_filter.py
python test.tool.metadata_filter.py
```

---

#### MCP Client Test

```bash
python test.mcp_client.py
```

---

#### MCP Server Test

```bash
python test.mcp_server.py
```

---

#### Full System Test

```bash
python test.app.py
```

---

## Run API

```bash
./run_api.sh
```

---

## TEST API

```bash
./test_api.sh
```

---


Example:

```
Query: iphones with good battery life
```

Pipeline:

```
Planner → DAG
Executor → Tools
Context → Aggregation
LLM → Final Answer
```

---

## Architecture Summary

```
                ┌──────────────┐
                │  User Query  │
                └──────┬───────┘
                       ↓
            ┌─────────────────────┐
            │   MCP Client LLM    │
            │ (DAG Planner)       │
            └────────┬────────────┘
                     ↓
            ┌─────────────────────┐
            │  Graph Executor     │
            │ (DAG Runtime)       │
            └────────┬────────────┘
                     ↓
        ┌──────────────────────────────┐
        │       MCP Server Tools       │
        │ VECTOR / WEB / DB / META    │
        └────────┬─────────────────────┘
                 ↓
           ┌──────────────┐
           │   Context     │
           └──────┬───────┘
                  ↓
        ┌────────────────────┐
        │ Final LLM Answer   │
        └────────────────────┘
```

---

## Future Improvements

* Multi-node distributed MCP servers
* Remote tool execution (Kubernetes / Docker swarm)
* Persistent graph caching
* Tool memory / reinforcement planner
* Better DAG validation layer
* Streaming execution context

---


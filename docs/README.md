
---

# 📦 src — Codebase Overview

Orion’s core is a **modular, interface-driven MCP orchestration system** built using a **DDD-inspired architecture**.

It is designed around:

* strict separation of concerns
* pluggable components
* registry-based tool discovery
* testable orchestration layers

---

## 🧠 High-Level Flow

```
main.py
   ↓
components/app.py
   ↓
MCP Client → Plan → Graph Executor → Tools → LLM Response
```

---

# 🧩 Architecture Layers

## 1. domain/ (Pure Core Logic)

Contains **framework-free business logic**:

* Query, Context
* Tool definitions
* RetrievalPlan (DAG structure)
* SearchAnswer
* Input/Output contracts

👉 No infrastructure, no LLM, no external dependencies.

---

## 2. application/ (Use Cases)

Implements orchestration logic:

* SearchUseCase → main entry for query execution
* SearchResponse → structured output

👉 This layer connects domain → MCP execution.

---

## 3. components/ (System Wiring Layer)

This is the **composition root**.

It is responsible for:

* building MCP client/server
* injecting infrastructure implementations
* connecting graph executor
* exposing FastAPI app

👉 Think of this as “the bootstrap layer”.

---

## 4. infrastructure/ (Concrete Implementations)

Contains all real implementations:

### real/

* MCP client (LLM-driven planner)
* MCP server (tool execution runtime)
* Graph executor (DAG execution engine)
* HTTP client (external APIs)
* Tool implementations (vector, web, DB, metadata)

### dummy/

* mocked versions for testing without LLM / external APIs

---

# 🧠 Core Concept: Registry System

Orion heavily uses **registry-based architecture** to avoid hardcoded dependencies.

---

## 🔧 What is a Registry?

A registry is a **central mapping system** that connects:

```
Tool Name → Tool Implementation
```

Instead of hardcoding tool calls, everything is resolved dynamically.

---

## 🧱 Main Registries in the System

### 1. Tool Registry

Located in:

```
infrastructure/real/mcp_server/tools/core/
```

Key files:

* `tool_information_registry.py`
* `tool_request_factory_registry.py`
* `tool_output_registry.py`

### What it does:

It maps:

```
ToolName → Tool metadata + execution strategy
```

This allows MCP to:

* discover available tools dynamically
* construct tool requests at runtime
* route execution without hardcoding logic

---

## 2. Tool Information Registry

Defines:

* tool name
* inputs/outputs
* description
* schema

👉 Used by the MCP planner to decide WHICH tool to use.

---

## 3. Tool Request Factory Registry

Maps:

```
Tool → Request Builder
```

Each tool has a factory that:

* builds validated request objects
* ensures correct input formatting
* isolates tool-specific logic

👉 This is what enables clean DAG node execution.

---

## 4. Tool Output Registry

Handles:

* normalizing tool outputs
* converting raw results → domain objects
* ensuring consistent response formats

---

# ⚙️ MCP Execution Model (Important)

The system works as a **dynamic DAG execution engine**:

```
LLM Planner
   ↓
RetrievalPlan (DAG)
   ↓
Graph Executor
   ↓
Registry resolves tools
   ↓
Tool execution
   ↓
Aggregated context
   ↓
Final LLM response
```

---

# 🧠 Why Registries Matter

This design enables:

### ✅ No hardcoded tool logic

Everything is resolved dynamically

### ✅ Easy testing

You can swap:

* real tools → dummy tools
* LLM → mocked planner

### ✅ Extensibility

Adding a tool =

1. implement tool
2. register it
3. done (no pipeline changes)

### ✅ Clean MCP separation

Planner doesn’t know execution details

---

# 🔌 Component Construction Pattern

Everything is built in layers:

### Step 1 — Define domain models

Query, Tool, Plan, Context

### Step 2 — Register tools

ToolRegistry maps everything

### Step 3 — Inject infrastructure

components/app.py wires:

* MCP client
* MCP server
* graph executor

### Step 4 — Execute DAG

Graph executor resolves everything via registry

---

# 🧪 Testing Alignment

Because of registry + interface design:

* tools can be mocked easily
* MCP client can be isolated
* DAG execution is deterministic
* unit tests don’t require real LLM

---

# 🧠 Design Summary

Orion is:

* **DDD-inspired**
* **registry-driven**
* **interface-based MCP system**
* **fully modular DAG executor**

Registries are the core abstraction that enable:

> dynamic tool orchestration without coupling or hardcoded logic

---


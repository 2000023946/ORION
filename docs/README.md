
---

# 📦 src — Codebase Overview

This module contains the **core MCP orchestration system** of Orion.

It is built using a **modular, interface-driven architecture** (DDD-inspired), separating:

* domain logic
* application use cases
* infrastructure implementations
* tool execution layer

This structure improves **testability, isolation, and maintainability**.

---

## 🧠 High-Level Structure

```
main.py → components/app.py → MCP Client → Graph Executor → Tools → LLM Response
```

---

## 📁 Key Layers

### 🧩 domain/

Core business models (pure logic, no dependencies)

* Query, Context, Tool, RetrievalPlan
* SearchAnswer, Input/Output contracts

---

### ⚙️ application/

Use cases / orchestration logic

* SearchUseCase
* SearchResponse

---

### 🧱 components/

System wiring (entry points + infrastructure composition)

* MCP client/server wiring
* Graph executor integration
* FastAPI app setup

---

### 🔌 infrastructure/

Concrete implementations

* LLM client (Groq)
* HTTP client
* MCP client/server
* Graph executor
* Tool implementations

Includes both:

* real/ → production implementations
* dummy/ → test/mocked versions

---

### 🛠 tools (inside infrastructure/real/mcp_server/tools)

Execution layer for MCP tools:

* vector search (semantic retrieval)
* db filter (structured filtering)
* metadata filter
* web search

---

### 🔗 ports/

Interface definitions (contracts)

Used to decouple:

* MCP client/server
* Graph executor
* Tool execution layer

Enables easy mocking in unit tests.

---

## 🧪 Testing Alignment

This structure supports:

* high unit test coverage (~95%)
* isolated component testing
* mock-based LLM + tool testing
* deterministic DAG execution tests

---

## 🧠 Design Philosophy

* Clean separation of concerns
* Interface-driven architecture
* MCP-based orchestration
* Pluggable tool system
* Fully testable graph execution layer

---

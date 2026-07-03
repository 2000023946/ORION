
---

# 🚀 Orion

**Orion** is an MCP-based dynamic retrieval system that uses LLM-driven orchestration to execute intelligent search strategies across multiple tools.

Instead of a fixed pipeline, Orion builds and executes **dynamic retrieval DAGs** using the Model Context Protocol (MCP), enabling adaptive querying across:

* Vector (semantic) search
* Structured database filtering
* Metadata refinement
* Web search integration

All tools are orchestrated through a central MCP execution layer that plans, executes, and aggregates results into a final response.

---

# 📌 Architecture

```
User Query → MCP Planner → DAG Execution → Tool Layer → Context → Final LLM Answer
```

---

## 📄 System Architecture

System architecture diagrams and detailed design docs are available in:

```
./docs
```

---


# 🚀 Run the Application (Demo Mode)

This is the **recommended way to start Orion**.

## 1. Prerequisites

* Docker installed and running

---

## 2. API Keys

You need API keys for:

* Groq (LLM)
* Tavily (web search)

Create a `.env` file in the root directory:

```bash
LLM_API_KEY=your_groq_api_key
WEB_API_KEY=your_tavily_api_key
```

---

## 3. Start the system

```bash
docker compose up --build
```

---

## 4. Open the app

* Frontend UI → [http://localhost:3000](http://localhost:3000)
* Backend API → [http://localhost:8000](http://localhost:8000)

---

# 🧪 Advanced Usage (Development + Testing)

This section is only needed if you want to **modify internals, run components independently, or debug MCP behavior**.

---

## ⚠️ Full Development Setup Required

To run any scripts or tests, you must have the full environment set up:

### 1. Docker Services

* Docker installed and running
* MongoDB running via Docker Compose (recommended)

### 2. API Keys

You must configure:

```bash
LLM_API_KEY=your_groq_api_key
WEB_API_KEY=your_tavily_api_key
```

inside `.env`

---

### 3. Python Environment

All testing requires a local Python environment:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

# 🧪 Testing Overview

Orion includes **~95% unit test coverage** across the core system.

---

## 🧪 Unit Tests (Core System Validation)

Unit tests validate individual components in isolation:

* MCP Planner
* DAG Executor logic
* Tool routing layer
* Mocked LLM interactions
* Vector / DB / metadata abstractions

This is the **main test suite for correctness and stability**.


---

## 🧪 Scripts (System Utilities)

The `scripts/` folder provides utilities for interacting with the system directly.

Main uses:

* Run API-level tests
* Validate tool execution
* Test MCP client/server behavior
* Quick system checks without full test suite

Example:

```bash
./scripts/run_test.sh
```

You can also use scripts to run the API independently for debugging.

---

## 🔬 Integrated Tests (Full System Components)

The `tests/integrated/` suite allows you to run **each MCP system component independently**, including:

* MCP Client
* MCP Server
* Graph Executor
* Tool execution layer (vector, DB, metadata, web)

These tests are designed for **deep debugging and execution tracing**, not just correctness.

Use them to:

* inspect DAG execution step-by-step
* validate tool chaining behavior
* debug orchestration issues
* test real system flows end-to-end at component level

---

### ⚠️ Integrated, Unit, Scripts Requirements

To run integrated, unit, scripts tests you need:

* Python venv activated
* Dependencies installed (`requirements.txt`)
* Docker running OR MongoDB running locally
* `.env` file with API keys configured

---

# 🧠 Key Idea

* **Frontend demo** → shows full system working end-to-end
* **Unit tests (~95%)** → ensure core MCP logic is correct and stable
* **Scripts** → quick API/system validation tools
* **Integrated tests** → deep component-level debugging of MCP orchestration

---

# ✅ Summary

| Mode                      | Purpose                               |
| ------------------------- | ------------------------------------- |
| Frontend (localhost:3000) | Live demo / UI experience             |
| scripts/                  | API + system utilities                |
| scripts/run_test.sh       | Main unit test runner                 |
| tests/unit                | Core logic validation (~95% coverage) |
| tests/integrated          | Full MCP component-level debugging    |

---
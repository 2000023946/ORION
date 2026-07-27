

---

# Orion

**Orion** is a cloud-scalable, MCP-based dynamic retrieval system that uses LLM-driven orchestration to execute intelligent search strategies across multiple tools.

Designed for high-throughput enterprise environments, Orion replaces fixed pipelines with **dynamic retrieval DAGs**. It leverages a load-buffered architecture (API Gateway + Message Queue) and a Redis edge cache to handle massive concurrent traffic, while utilizing asynchronous Model Context Protocol (MCP) execution to adaptively query across:

* **Vector (semantic) search**
* **Structured database filtering**
* **Metadata refinement**
* **Web search integration**

Built on pragmatic distributed systems principles, all I/O-bound tools are co-located for ultra-fast native `async` execution, while heavy ML compute is isolated into standalone services. The central MCP orchestration layer plans, executes, and aggregates these results into a lightning-fast final response without choking the event loop.

---

# System Architecture

```
User Query → MCP Planner → DAG Execution → Tool Layer → Context → Final LLM Answer
```

Here’s a tighter version that keeps the meaning but makes it very minimal:

---
## System Design

Orion follows a **modular, interface-driven (DDD-style) architecture** with clear separation between domain, application, and infrastructure layers. This enables high testability, maintainability, and pluggable MCP tool execution.

Full architecture details:

```
./docs
```

---

## Regional Cloud Architecture

Orion uses a decoupled, buffered architecture designed to survive massive enterprise traffic spikes without dropping requests:

* **Edge Cache & API Gateway:** Instantly serves repeated queries to shield downstream compute resources from redundant work.
* **Message Queue Buffer:** Acts as a shock absorber. By decoupling request ingestion from execution, it prevents expensive 3-second search queries from exhausting the server's connection pool.
* **Co-Located Search Engine:** Groups I/O-bound MCP tools on a single pod for zero-latency `async` communication, avoiding the nanoservice trap of excessive network hops.
* **Isolated Compute & State:** Keeps heavy ML embedding models and enterprise databases strictly external, preserving the core cluster's ability to horizontally scale.


> **Note:** For deep-dive technical configurations, infrastructure manifests, and detailed deployment steps, please refer to the comprehensive documentation located in the `./docs/cloud/` directory of the project repository.

---

## GIF Demo

A short demo showing a full end-to-end query flow through the MCP system:

* User query input in the frontend
* MCP planner generating a retrieval plan (DAG)
* Tool execution (vector / DB / web / metadata)
* Final aggregated LLM response

This demonstrates how Orion dynamically orchestrates tools and executes structured reasoning steps in real time.

![Orion Demo](assets/demo.gif)

---


# Run the Application (Demo Mode)

This is the **recommended way to start Orion**.

## 1. Prerequisites

* Docker installed and running

---

## 2. API Keys

The API keys for:

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

## Local Kubernetes Deployment (Minikube)

To spin up the cloud-scalable architecture locally on a Mac, ensure Minikube is installed and active, then apply all cluster manifests:

```bash
# Start the local cluster environment
minikube start

# Deploy all services, configurations, and infrastructure nodes
kubectl apply -f .

```

### Exposing the Endpoints

Because the architecture relies on a decoupled ingress and real-time telemetry extraction, establish network tunnels by running these port-forwards in separate terminal sessions:

1. **API Gateway Ingress** (Exposes the edge entry point to submit requests):
```bash
kubectl port-forward deployment/api-gateway 8000:8000

```


2. **Prometheus Telemetry Endpoint** (Strictly required by the load-testing script to parse system metrics and populate the performance dashboard):
```bash
kubectl port-forward deployment/prometheus 9090:9090

```



With both tunnels active, the automated Locust test harness seamlessly interacts with the API gateway while simultaneously scraping live CPU, memory, and duration metrics directly from the Prometheus endpoint to generate the comprehensive dashboard.

--- 

## Performance Benchmarking & Load Testing

To validate architectural scaling boundaries empirically, Orion relies on a dynamic, highly automated load-testing suite managed entirely inside the `./locust` directory.

Executing the benchmarking protocol requires running a single automated script:

```bash
python3 run_sequential_tests.py

```

This execution runner sequentially triggers tests across scaling brackets (100, 250, 500, 1000, and 2000 concurrent users), measuring end-to-end throughput alongside per-component CPU constraints, execution intervals, and active connection latencies via Prometheus scraping.

All outputs are automatically structured and archived hierarchically within the metrics suite:

```text
.
├── baseline_results
│   ├── 100_users/          # Outbound CSVs, exceptions, and prometheus captures
│   ├── 250_users/
│   ├── 500_users/
│   ├── 1000_users/
│   ├── 2000_users/
│   └── comprehensive_metrics_dashboard.html
├── collect_prometheus.py   # Automated telemetry data extractor
├── generate_comparison_report.py
├── locustfile.py           # Dynamic query runner simulation
└── run_sequential_tests.py # Primary automation harness

```

Upon completion, the orchestration runner dynamically compiles raw metrics logs and pulls data from Prometheus, auto-generating a standalone visual file: `comprehensive_metrics_dashboard.html`. This report provides localized visualization of failure distributions, resource-to-request trends, and cache hit/miss advantages across massive traffic gradients.

---

# Advanced Usage (Development + Testing)

This section is for to **modify internals, run components independently, or debug MCP behavior**.

---

## Full Development Setup Required

To run any scripts or tests, a full environment set up:

### 1. Docker Services

* Docker installed and running
* MongoDB running via Docker Compose (recommended)

### 2. API Keys

Configure:

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

# Testing Overview

Orion includes **~95% unit test coverage** across the core system. The results can 
be seen in `htmlcov/index.html`

---

## Unit Tests (Core System Validation)

Unit tests validate individual components in isolation:

* MCP Planner
* DAG Executor logic
* Tool routing layer
* Mocked LLM interactions
* Vector / DB / metadata abstractions

This is the **main test suite for correctness and stability**.


---

## Scripts (System Utilities)

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

Scripts can also be used to run the API independently for debugging.

---

## Integrated Tests (Full System Components)

The `tests/integrated/` suite runs **each MCP system component independently**, including:

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

Example:

```bash
python3 test.graph_executor.py
```

---

# Key Idea

* **Frontend demo** → shows full system working end-to-end
* **Unit tests (~95%)** → ensure core MCP logic is correct and stable
* **Scripts** → quick API/system validation tools
* **Integrated tests** → deep component-level debugging of MCP orchestration

---

# Summary

| Mode                      | Purpose                               |
| ------------------------- | ------------------------------------- |
| Frontend (localhost:3000) | Live demo / UI experience             |
| scripts/                  | API + system utilities                |
| scripts/run_test.sh       | Main unit test runner                 |
| tests/unit                | Core logic validation (~95% coverage) |
| tests/integrated          | Full MCP component-level debugging    |

---

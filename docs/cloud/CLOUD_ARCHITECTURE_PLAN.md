
---

# Orion: Distributed Architecture Evaluation Methodology

## Overview

The next evolution of Orion targets a cloud-native distributed Model Context Protocol (MCP) architecture designed for horizontal scalability, fault isolation, and efficient resource utilization.

The migration follows an evidence-driven approach: **a component is extracted into a microservice only when experimental measurements demonstrate a measurable benefit.**

The goal is not to maximize the number of services, but to identify the architecture that provides the best balance between performance, scalability, and operational complexity.

---

# I. Target Architecture

If benchmark results justify service decomposition, Orion will transition toward the following architecture.

## Edge and Orchestration Layer

### Load Balancer

Distributes incoming requests across multiple API instances to provide availability and prevent request bottlenecks.

### API Gateway

Provides a lightweight entry point into the MCP workflow and manages request routing.

### Redis Cache

Stores frequently requested results, generated plans, and tool outputs to reduce repeated computation.

---

## Core Compute Services

### LLM Planner Service

The planner is isolated due to its high computational cost and potential scaling impact. Independent deployment allows planner capacity to scale separately from other system components.

### Graph Execution Engine

The graph executor manages MCP workflow execution. Separation allows independent scaling and prevents orchestration workloads from competing with request ingestion resources.

---

## MCP Tool Services

Specialized tools may be deployed independently when measurements demonstrate scaling advantages.

Potential services include:

* **Metadata Filtering Service:** Handles lightweight filtering operations.
* **Vector Search Service:** Handles vector retrieval workloads.
* **Web Search Service:** Handles external, latency-variable requests.

---

## Embedding and Storage Layer

### Embedding Service

Embedding generation is isolated due to its CPU and memory requirements, allowing independent scaling of model inference workloads.

### Vector Database

The local FAISS-based storage layer may transition to a managed vector database solution for production deployment and horizontal scalability.

---

# II. Experimental Evaluation Methodology

The final architecture will be determined through controlled benchmarking.

## Phase 0: Controlled Monolithic Baseline

A stable monolithic implementation will be created as the experimental baseline.

The baseline will include:

* API Gateway
* Graph Executor
* Planner
* Vector Search

External dependencies will be replaced with controlled mock services.

Mock services will:

* Introduce configurable latency.
* Return realistic responses.
* Avoid external network dependencies.
* Produce repeatable benchmark behavior.

---

## Phase 1: Instrumentation

All major components will collect performance metrics.

Tracked measurements include:

* Request start and completion time.
* Component execution duration.
* Memory utilization.
* Request failure information.

Example:

| Component       | Average Time | Memory |
| --------------- | -----------: | -----: |
| API             |         4 ms |  30 MB |
| Graph Executor  |        28 ms | 120 MB |
| Planner         |        18 ms |  45 MB |
| Vector Search   |       110 ms | 3.8 GB |
| Redis           |         2 ms | 150 MB |
| Mock LLM        |       300 ms |  20 MB |
| Mock Web Search |       520 ms |  15 MB |

---

## Phase 2: Baseline Load Testing

Locust will generate repeatable workloads against the monolithic baseline.

Testing levels:

* 10 users
* 50 users
* 100 users
* 250 users
* 500 users
* 1000 users

Collected metrics:

* Requests per second
* Average latency
* p95 latency
* Failure rate
* Component execution time

Baseline results will be preserved for all future comparisons.

---

## Phase 3: Independent Service Evaluation

Each microservice candidate will be evaluated independently.

Each experiment begins from the original monolithic baseline.

| Experiment | Change                 |
| ---------- | ---------------------- |
| A          | Extract Graph Executor |
| B          | Extract Planner        |
| C          | Extract Vector Search  |
| D          | Extract LLM Service    |
| E          | Extract Web Search     |

Each configuration will be benchmarked and compared against the baseline before returning to the original system.

---

## Phase 4: Final Architecture Construction

The final architecture will include only components that demonstrated measurable improvements during independent experiments.

Possible benefits evaluated:

* Increased throughput
* Reduced latency
* Improved memory isolation
* Improved failure handling
* Independent scaling capability

---

## Phase 5: Final Validation

The final architecture will be tested using identical workloads.

| Metric          | Monolith Baseline | Final Architecture |
| --------------- | ----------------- | ------------------ |
| Throughput      |                   |                    |
| Average Latency |                   |                    |
| p95 Latency     |                   |                    |
| Failure Rate    |                   |                    |

The objective is to determine whether service decomposition provides measurable improvement over the original design.

---

# III. Final Engineering Report

The final report will include:

* Architecture diagrams of baseline, experiments, and final deployment.
* Component-level performance measurements.
* Locust benchmark results.
* Latency and throughput comparisons.
* Memory utilization analysis.
* Evidence-based service decomposition decisions.

Each architectural decision will be supported by experimental results rather than assumptions.

---

# Payload Simulation Consideration

To accurately evaluate memory behavior during Phase 0, mock services should use representative payload sizes.

Recommended approach:

* Small payloads: control messages and metadata (~1–10 KB)
* Medium payloads: retrieval results and tool outputs (~100 KB–1 MB)
* Large payloads: embedding vectors and document context (~1–10 MB)

The selected payload sizes should match expected production workloads so memory measurements reflect realistic system behavior.

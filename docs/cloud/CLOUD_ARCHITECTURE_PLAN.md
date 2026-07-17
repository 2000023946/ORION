Here is the combined document. It merges your target distributed architecture with the rigorous experimental methodology required to justify it, creating a single, cohesive engineering proposal.

---

## Orion: Enterprise Distributed Architecture & Evaluation Methodology

The next evolution of Orion is a cloud-native, distributed Model Context Protocol (MCP) architecture. It is designed for high throughput, horizontal scalability, and enterprise-scale deployment. The system prioritizes concurrent load handling, clean domain isolation, and efficient resource scaling over purely optimizing single-request latency.

However, this architectural target must be proven, not assumed. The entire migration operates as a rigorous research experiment guided by one core principle: **Only split a component into a microservice if the measurements justify it.**

---

### I. System Vision & Target Architecture

If the benchmark data fully validates the decomposition, the final system will be organized into the following layers:

**Edge & Orchestration Layer**

* **Load Balancer:** Distributes incoming traffic across multiple API instances to ensure high availability and prevent ingestion bottlenecks.
* **API Gateway:** Acts as a lightweight orchestration layer forwarding requests into the MCP pipeline.
* **Redis Edge Cache:** Intercepts repeated query responses, LLM-generated plans, and tool execution results to drastically reduce redundant computational overhead.

**Core Compute Services**

* **LLM Planner Service:** Isolated as an independent service due to its high inference cost (averaging ~3s per request) and its role as a primary scaling bottleneck.
* **Graph Execution Engine:** Processes MCP workflows rapidly via gRPC and task buses. It is physically separated from request handling to prevent tight coupling and preserve memory limits under extreme load.

**Specialized MCP Tool Microservices**
Tools are deployed as independent microservices to allow workload-specific scaling:

* **Metadata Filtering Service:** Handles lightweight, rapid queries.
* **Vector Search Service:** Handles moderately expensive I/O operations.
* **Web Search Service:** Manages highly variable, latency-heavy external calls.

**Embedding & Storage Migration**

* **Embedding Generation:** Isolated to scale appropriately for compute-heavy and memory-intensive operations (e.g., sentence-transformer models).
* **Vector Database:** Transitions from local, containerized FAISS storage to Pinecone for a fully managed, horizontally scalable, multi-region production environment.

---

### II. Microservice Evaluation Methodology

To build the final architecture, we will measure where every request spends its time and evaluate candidates individually.

#### Phase 0: Build a Controlled Monolith

Establish a stable baseline system that produces repeatable benchmark results.

* Build Orion as a single monolithic application containing the API, Graph Executor, Planner, and Vector Search.
* Replace external services with mock implementations (Mock LLM, Mock Web Search).
* Ensure mock APIs sleep for configurable delays.
* Ensure mock APIs return realistic JSON responses.
* Ensure mock APIs never call the internet.

#### Phase 1: Add Instrumentation

Instrument every major component to track performance metrics.

* Record the start time, end time, and duration for every request.
* Optionally record memory usage before and after execution.

**Example Component Timing Output:**

| Component | Avg Time | Memory |
| --- | --- | --- |
| API | 4 ms | 30 MB |
| Graph Executor | 28 ms | 120 MB |
| Planner | 18 ms | 45 MB |
| Vector Search | 110 ms | 3.8 GB |
| Redis | 2 ms | 150 MB |
| Mock LLM | 300 ms | 20 MB |
| Mock Web Search | 520 ms | 15 MB |

#### Phase 2: Establish the Baseline

Run Locust against the Phase 0 monolith to collect the permanent baseline metrics.

* Test at intervals of 10, 50, 100, 250, 500, and 1000 users.
* Collect throughput (requests/sec), average latency, p95 latency, failure rate, and component timings.
* Save these results permanently; never overwrite them.

#### Phase 3: Evaluate Candidates Independently

Always start from the original Phase 0 monolith. Do not build on previous experiments.

* **Experiment A:** Split only the Graph Executor. Run benchmarks, compare with baseline, and record the decision. Return to monolith.
* **Experiment B:** Split only the Planner. Run benchmarks, compare, and record. Return to monolith.
* **Experiment C:** Split only Vector Search. Run benchmarks, compare, and record. Return to monolith.
* **Experiment D:** Split only the LLM. Run benchmarks, compare, and record. Return to monolith.
* **Experiment E:** Split only Web Search. Run benchmarks, compare, and record. Return to monolith.

#### Phase 4: Build the Final Architecture

Construct the final system utilizing only the specific services that demonstrated a measurable performance benefit during the independent experiments in Phase 3.

#### Phase 5: Final Validation

Benchmark the final architecture using the exact same Locust workloads to answer the ultimate question: *Does the final architecture outperform the original monolith?*

| Metric | Monolith Baseline | Final Architecture |
| --- | --- | --- |
| Throughput |  |  |
| Avg Latency |  |  |
| p95 Latency |  |  |
| Failure Rate |  |  |

#### Phase 6: Analyze the Results

Provide an evidence-based conclusion for every component.

**Example Analysis:**

| Component | Evidence | Decision |
| --- | --- | --- |
| Graph Executor | Throughput increased by 32% | Microservice |
| Planner | No measurable improvement | Keep in monolith |
| Vector Search | Lower latency and isolated memory usage | Microservice |

---

### III. Final Deliverables

The resulting engineering report will serve as a robust defense of the system's design and will include:

* **Architecture Diagrams:** Visualizations of the original monolith, simplified experimental configurations, and the final microservice topology.
* **Instrumentation Results:** Raw data covering per-component timing and optional memory usage.
* **Benchmark Results:** Locust outputs detailing throughput, average/p95 latency, and failure rates.
* **Comparison Tables:** Direct comparisons between the baseline and individual experiments, as well as the baseline versus the final build.
* **Evidence-Backed Decisions:** Explicit justifications detailing exactly why each service was kept in the monolith or extracted, relying strictly on collected measurements rather than generic distributed system principles.

---

To ensure the Phase 0 monolith accurately simulates the memory footprint of your background task serialization, do you want to define specific payload sizes for those Mock API JSON responses?
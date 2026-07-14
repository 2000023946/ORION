Here is the polished version of your architecture proposal report. I have refined the technical phrasing, formatted the document professionally, and integrated the new memory analysis section using the exact filenames corresponding to your uploaded screenshots.

---

# Architecture Scaling Proposal: Decoupling the Graph Executor

## 1. Executive Summary

Load testing on the core orchestration framework has identified a critical concurrency bottleneck. The system operates stably with clean linear scaling up to **1,000 concurrent users**, but experiences catastrophic performance degradation beyond this threshold. To break past this ceiling, we propose decoupling the CPU/mutex-bound `graph_executor` component from the main orchestrator into an isolated, independently scalable microservice.

---

## 2. The Concurrency Wall: The 1K User Ceiling

As documented in our core Locust load testing suite, the infrastructure performs optimally up to 1,000 concurrent users. At peak efficiency, it achieves a steady throughput of **~85–90 requests/second with a 0% failure rate**.

However, scaling from 1,000 to 2,000 concurrent users triggers severe thread thrashing:

* **Throughput Drop:** System capacity degrades as the system context-switches under heavy load.
* **Cascading Latency:** Aggregate response times skyrocket exponentially, hitting an unmanageable **20,000 ms (20 seconds)**.
* **Gateway Exhaustion:** The upstream API gateway suffers cascading connection timeouts, resulting in **170+ hard failures**.

![Locust Core Statistics](Screenshot 2026-07-14 at 3.50.21 PM.jpg)
*Figure 1: Core system metrics illustrating the sharp throughput collapse and failure spike past 1,000 users.*

---

## 3. Root Cause Analysis: The Graph Executor Bottleneck

Cross-referencing our Prometheus micro-metrics isolates the root cause directly to the system execution graph layer.

While individual data-retrieval utilities—such as the `vector_search_tool`, `metadata_filter_tool`, and `db_filter_tool`—maintain a flat, near-zero latency signature across all testing tiers, the `graph_executor` completely buckles under load.

![Prometheus Component Latency](Screenshot 2026-07-14 at 3.51.01 PM.png)
*Figure 2: Microservice component latency profile highlighting the exponential latency growth of the graph_executor.*

The `graph_executor`'s average execution delay shoots up sharply, crossing the high baseline of the web search tool and reaching **3,500 ms at 1,000 users**. Because the runtime engine relies on this component to manage state machines and handle LLM parallel dispatch, its internal latency blocks the synchronous event loop. This blocks connection pools down the line and triggers the macro timeouts shown in Figure 1.

---

## 4. Resource Profile: Memory Consumption Analysis

To ensure the bottleneck wasn't caused by memory leaks or container OOM (Out Of Memory) throttling, we analyzed resource footprint tracking across all components.

![Component Memory Footprint](Screenshot 2026-07-14 at 4.06.19 PM.png)
*Figure 3: Component memory consumption (MB) relative to concurrent user volume.*

The metrics confirm that **heap allocation is completely stable**. The memory footprint across all orchestration layers and sidecar tools remains uniform and flat up to 2,000 users, staying well below critical limits. This proves that the performance wall is strictly a **concurrency/compute bottleneck** (likely driven by lock contention or synchronous execution blocks within the graph) rather than a memory leak.

---

## 5. Proposed Architecture Target State

To scale past the 1,000-user barrier, we will execute the following system changes:

* **Microservice Extraction:** Refactor the `graph_executor` out of the main orchestrator codebase and deploy it as a dedicated, containerized microservice.
* **Targeted Kubernetes Auto-Scaling:** Implement a Horizontal Pod Autoscaler (HPA) targeting the new `graph_executor` deployment. This allows the cluster to scale compute resources horizontally under load without wasting overhead duplicating the low-latency tools (`vector_search_tool`, `db_filter_tool`).
* **Asynchronous Communication & Boundary Isolation:** Decouple the synchronous API gateway path. Shift the orchestrator-to-executor handoff to an asynchronous pattern or optimized gRPC streaming connection pool to eliminate upstream gateway blocking during parallel dispatch phases.
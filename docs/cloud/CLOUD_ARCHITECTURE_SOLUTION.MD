
---

# Orion Distributed Architecture Retrospective

## Overview

The evolution of Orion demonstrates the iterative process of designing distributed systems. Through successive experiments, the architecture moved from a local monolithic implementation toward a scalable cloud-oriented design.

The major design decisions were guided by measured system behavior, resource constraints, and workload characteristics rather than assumptions about microservice architecture.

---

# 1. Local Benchmarking Limitations

Initial Locust testing against a local monolithic deployment provided limited insight into production scalability.

A monolithic application often performs well on a single machine because:

* Components communicate through local memory.
* Network serialization is avoided.
* Shared resources are immediately available.

However, this behavior does not represent cloud deployment conditions where systems must handle:

* Container resource limits.
* Network communication overhead.
* Independent service scaling.
* Resource contention.

The primary limitation of the monolith was reduced fault isolation. A failure in a memory-intensive component, such as an LLM planner or embedding model, could consume resources available to the entire application and affect unrelated workloads.

---

# 2. Microservice Granularity and gRPC Overhead

The first decomposition strategy separated individual MCP tools into independent microservices.

The design isolated:

* Metadata filtering
* Vector search
* Web search
* Additional MCP tools

However, evaluation revealed that this approach introduced unnecessary service fragmentation.

The isolated components were primarily I/O-bound workloads. Splitting them into separate services did not provide additional computational capacity because the workload was limited by external dependencies rather than local processing.

The resulting overhead included:

* Additional network communication.
* Serialization and deserialization costs.
* Increased operational complexity.

The architecture was adjusted by grouping related I/O-bound components together and using asynchronous execution within the service boundary.

---

# 3. Search Latency and Queue-Based Processing

After consolidating I/O workloads, testing revealed that search execution remained a significant bottleneck, with individual requests requiring approximately three seconds to complete.

Under high concurrency, synchronous request handling caused:

* Increased connection utilization.
* Executor saturation.
* Higher request failure rates.

A message queue was introduced between request ingestion and workload execution.

The queue provided:

* Request buffering during traffic spikes.
* Separation between client traffic and processing capacity.
* Controlled execution of long-running workloads.

The API Gateway could accept requests rapidly while worker services processed tasks at a sustainable rate.

---

# 4. Redis-Based Edge Caching

Although queue-based processing improved stability, repeated queries still generated unnecessary computation.

To reduce redundant processing, an edge cache layer was introduced.

The Redis cache allows:

* Repeated queries to bypass the processing pipeline.
* Reduced workload sent to downstream services.
* Lower response latency for cached requests.

This optimization improved resource efficiency by avoiding repeated execution of identical workloads.

---

# 5. Final Architecture Principles

The final architecture follows a selective isolation strategy:

**Components are separated only when measurable benefits justify the additional operational complexity.**

Final design decisions:

* I/O-bound MCP tools remain grouped to minimize communication overhead.
* Vector storage and metadata databases are externalized to managed storage systems for scalability and persistence.
* Embedding generation is isolated due to high memory requirements and model size.
* Queue-based processing is used for long-running workloads requiring traffic buffering.
* Redis caching reduces unnecessary repeated computation.

---

# Conclusion

The Orion architecture evolved through multiple design iterations:

1. Local monolithic implementation for baseline measurement.
2. Excessive service decomposition that introduced unnecessary overhead.
3. Consolidation of related workloads.
4. Introduction of asynchronous queues for workload isolation.
5. Selective microservice extraction based on resource requirements.

The final architecture demonstrates that effective distributed system design is not defined by the number of services deployed. Instead, successful decomposition requires understanding workload characteristics, identifying resource bottlenecks, and introducing distributed components only where they provide measurable improvements.

---

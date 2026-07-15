
---

# Architectural Benchmark Report: Monolith vs. Microservice (Local Infrastructure)

This report analyzes the performance characteristics of a multi-agent LLM application tested under extreme load (up to 2,000 concurrent users). It directly compares a monolithic in-memory architecture against a containerized microservice mesh running on a localized virtual network.

## 1. System Throughput & Network Saturation

![Microservice Core Stats](microservice_core_stats.png)
![Monolith Core Stats](core_stats.png)
*Metric Source: Locust Core Statistics (Throughput, Average Response Time, Failures)*

This section measures the "front door" experience for the user. It highlights the fundamental difference between sharing memory and sharing a network.

### The Analysis

* **The Microservice Collapse:** At 1,000 users, the microservice architecture suffered a catastrophic queueing failure. Throughput collapsed from 35 to 15 requests per second, response times spiked to nearly 50 seconds, and over 1,500 connections simply dropped (failed). This occurred because the virtual network bridge on the local machine ran out of TCP sockets attempting to route thousands of internal gRPC connections simultaneously.
* **The Monolith Advantage:** The monolith absorbed the exact same traffic spike flawlessly. It maintained a **0% failure rate** past 1,000 users and pushed throughput smoothly past 80 requests per second.
* **The Physical Reason:** A monolith does not use network sockets to communicate internally. It passes memory pointers in nanoseconds. The microservice mesh was bottlenecked not by code, but by the physical limits of local virtual networking.

---

## 2. Internal Execution vs. External Queueing

![Microservice Component Latency](microservice_component_latency.png)
![Monolith Component Latency](component_latency.png)
*Metric Source: Prometheus Component Latency*

This section isolates the execution time of individual Python components (e.g., `vector_search_tool`, `mcp_plan`) from the total user wait time, revealing a critical architectural paradox.

### The Analysis

* **Microservices (Clean but Queued):** Notice how flat and horizontal the lines are for the microservice. The `vector_search_tool` stayed incredibly fast (~50ms) regardless of how many users hit the system. The components are perfectly isolated inside their own containers. However, the users experienced massive delays because their requests were trapped outside in the API Gateway network queue before the components ever saw them.
* **Monolith (Fast but Starved):** Notice how the monolith lines curve upwards diagonally as user load increases. Because 1,000 users are trapped in the exact same Python process, the internal functions are starved for CPU cycles. The operating system is constantly context-switching, making individual tasks take longer.
* **The Physical Reason:** Microservices protect code execution speed via container isolation, pushing the bottleneck to the network queue. Monoliths eliminate the network queue, pushing the bottleneck directly onto the CPU.

---

## 3. The Payload Serialization Tax

![Microservice Component Latency](microservice_memory.png)
![Monolith Component Latency](memory.png)
*Metric Source: Prometheus Component Memory*

This section tracks the active RAM utilization of individual components under load, highlighting the hidden computational cost of separating services.

### The Analysis

* **Microservice Memory Bloat:** Right at the 500-user mark, specific microservice components (like `mcp_plan` and `metadata_filter_tool`) experienced a **500% spike in memory footprint** (jumping to 0.25 MB). This is the physical weight of backlogged network traffic. Every incoming request must be buffered in RAM, deserialized from network bytes, parsed into JSON/Protobuf, and converted into Python dictionaries.
* **Monolith Memory Efficiency:** The monolith's memory lines crash toward 0.00 MB as the load increases. Because everything runs in a single process, the global garbage collector works efficiently to destroy temporary objects, and no translation or network buffering is required to pass data between functions.
* **The Physical Reason:** Microservices pay a heavy "Serialization Tax." Separating components requires you to duplicate data in RAM across network boundaries just to read it.

---

### Final Architectural Conclusion

On a localized, single-machine infrastructure, the **Monolith** will mathematically outperform the **Microservice mesh** in every major category (throughput, latency, and memory) because it avoids the virtualization and serialization overhead.

However, the microservice bottlenecks identified here—network socket exhaustion and gateway queueing—are strictly horizontal scaling problems. When deployed to a multi-node cloud environment (such as AWS EKS), the microservice architecture allows these specific network queues to be distributed across infinite physical hardware, unlocking a scale the monolith could never achieve.
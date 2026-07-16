### **Load Test Analysis: The "Microservice Tax" on Constrained Hardware**

**Objective:** To evaluate system stability and resource consumption between an In-Memory (Monolithic) architecture and a Microservice architecture under heavy user load within a strict 4GB RAM environment.

---
![In memory Vector DB Core Stats](microservice_core_stats.png)
![Service Vector DB Core Stats](vector_db_service.png)

#### **Executive Summary**

The testing reveals a stark contrast in how systems fail under physical memory constraints. While microservices offer superior granular scaling in cloud environments, deploying them on severely restricted local hardware introduces an "infrastructure tax" that drastically accelerates system collapse.

#### **Performance Comparison Matrix**

| Metric | Scenario 1: In-Memory (The Sponge) | Scenario 2: Microservice (The Glass) |
| --- | --- | --- |
| **Architecture** | Shared 4GB RAM Pool | Sliced RAM (Standalone Vector DB) |
| **Peak Latency** | ~50,000 ms (50 seconds) | ~0 ms *(False positive due to crash)* |
| **Throughput** | Bottlenecked (Queuing) | 500+ req/s *(Error generation rate)* |
| **Failure Count** | ~1,700 (Network Timeouts) | 60,000+ (Hard Crashes) |
| **System State** | Degraded but actively processing | **OOMKilled** (Complete collapse) |

---

### **Detailed Findings**

#### **1. The "Sponge" Model (In-Memory Monolith)**

By sharing the global 4GB memory pool, the system utilized available RAM dynamically without rigid container boundaries.

* **Behavior:** The system absorbed massive traffic spikes by aggressively queuing incoming requests.
* **Outcome:** The system bent but did not break. While response times degraded to nearly a minute at 1,000 users, the architecture fought to stay alive. The resulting ~1,700 failures were standard client-side timeouts, not server deaths.

#### **2. The "Glass" Model (Standalone Microservice)**

Extracting the vector database into a separate Kubernetes pod immediately locked up ~500 MB of the RAM pool, starving the API Gateway and Executor of their operational buffer.

* **Behavior:** Unable to queue requests dynamically, the system hit a hard memory wall and shattered instantly.
* **The "Fast Failure" Trap:** At 2,000 users, the metrics presented a dangerous illusion: throughput spiked and latency dropped to zero. In reality, the Linux kernel had terminated the pods (`OOMKilled`) due to memory exhaustion. The "throughput" was actually the dead server instantly rejecting connections and firing off 500 `502 Bad Gateway` errors per second.

### **Conclusion**

On hardware strictly limited to 3.9 GB of RAM, a monolithic (or in-memory) architecture is mathematically more resilient. The overhead of an extra operating system layer, container runtime, and network serialization required by the standalone microservice is sufficient to push a constrained system into an Out-Of-Memory death spiral.
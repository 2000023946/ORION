# Proposal: Ingestion Layer Resilience & Network Stack Optimization for Project Orion

## 1. Executive Summary & Problem Statement

During high-concurrency load testing (scaling up to 500 concurrent users), Project Orion’s asynchronous architecture experienced severe pipeline starvation. Locust telemetry revealed thousands of failed requests and massive response spikes, while KEDA reported a constant queue depth of `0/10`.

Root cause analysis proved that **the executor was not underperforming—it was starved of work** because the upstream `api-gateway` choked during sudden traffic bursts. Capped by reactive CPU-based autoscaling and restrictive default OS network settings, the API Gateway pods saturated their listening queues and dropped incoming TCP packets at the kernel level before application code could serialize tasks or push them to the Redis broker.

To solve this, we propose pre-scaling our ingestion layer, expanding kernel socket listening buffers, and implementing persistent TCP connection pooling.

---

## 2. Proposed Architectural Enhancements

### A. Pre-Scaling Ingestion Replicas (Bypassing Reactive Lag)

* **The Limitation:** Native Kubernetes CPU Horizontal Pod Autoscalers (HPA) operate on a reactive metrics polling loop (typically every 15 seconds). During instantaneous traffic spikes, the scheduler cannot spin up new pods fast enough to prevent socket overflow.
* **The Solution:** Adjust the `api-gateway` HPA baseline configuration to maintain a minimum pre-warmed pool (`minReplicas: 2` to `4`), guaranteeing immediate compute availability the moment traffic hits the cluster.

### B. OS Socket Backlog Expansion (`SOMAXCONN` Tuning)

* **The Limitation:** The default Linux kernel socket listener backlog (`SOMAXCONN`) restricts the size of the OS "waiting room" for fully established TCP connections waiting to be accepted by the application. Under heavy bursts, this buffer overflows immediately, forcing the kernel to drop incoming connection requests.
* **The Solution:** Inject a pod-level `securityContext` into the `api-gateway` deployment to safely scale the operating system socket backlog limit up to **4,096**:
```yaml
securityContext:
  sysctls:
  - name: net.core.somaxconn
    value: "4096"

```



### C. Persistent TCP Connection Pooling

* **The Limitation:** Continuously spinning up fresh TCP connections between the API Gateway, the downstream microservices, and Redis introduces severe CPU overhead, network latency, and connection exhaustion due to repeated three-way handshakes.
* **The Solution:** Enforce persistent, reused TCP connection pools across all outbound client drivers inside the API Gateway application code. This keeps communication channels open, drastically reduces handshake latency, and ensures high-throughput payload hand-off to the Redis queue.

---

## 3. Expected Impact & Verification Plan

1. **Elimination of Kernel-Level Drops:** Expanding `somaxconn` to `4096` ensures the OS can hold connection requests safely during bursts rather than rejecting them outright.
2. **Guaranteed Message Broker Ingestion:** With pre-scaled gateway pods and expanded buffers, incoming requests will successfully pass through the gateway and populate the Redis queue.
3. **Unblocking KEDA Autoscaling:** Once Redis registers the queue depth increase, KEDA will dynamically scale the `orion-executor` pods to process the workload concurrently, bringing system throughput and failure rates back to nominal levels.
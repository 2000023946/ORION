## Orion API Gateway & Executor: Load Testing & Bottleneck Analysis Report

### Executive Summary

Recent performance scaling tests on the Orion system demonstrated that optimizing network stacks (such as adjusting TCP socket backlogs and connection pooling) successfully eliminates network-level transport bottlenecks. However, high-concurrency load testing revealed a 100% failure rate under increased load.

The primary constraint is not network throughput, but **worker capacity and task execution time**. Because incoming request arrival rates vastly outpace the processing capability of single-threaded/single-CPU executor nodes, tasks accumulate into a rapidly growing queue, eventually triggering timeouts and system failures.

---

### Queue Dynamics & Mathematical Proof

To understand why the system saturates, we can model the rate of change of the task queue over time ($t$).

* **Incoming Request Rate**: Spawn rate of **$8$ requests per second** (as observed during the 8 users/second spawn rate test).
* **Processing Rate (Outgoing)**: Each complex orchestration request (involving MCP execution, LLM coordination, and vector searches) takes an average of **$3$ seconds** per task per worker. This means a single worker processes tasks at a rate of $\frac{1}{3}$ tasks per second.
* **Assumptions**: Assuming a baseline resource allocation of **1 node / 1 CPU per application instance** ($1$ executor worker).

#### Queue Growth Equation:

$$\text{Rate of Change} = \text{Incoming Rate} - \text{Outgoing Rate}$$

$$\frac{dQ}{dt} = 8t - \frac{t}{3}$$

$$\frac{dQ}{dt} = \frac{24t - t}{3} = \frac{23t}{3}$$

Because the incoming load ($\approx 8 \text{ req/s}$) is drastically higher than a single worker's capacity ($\approx 0.33 \text{ req/s}$), the queue size increases continuously without ever emptying. This structural deficit causes backpressure, request timeouts, and systemic failures.

---

### Load Test Evidence

The Locust report below captures the 40-users test run. Notice how the median response latency drops to a clean **4–5 ms**—this occurs because the API Gateway instantly accepts requests and pushes them to the Redis queue, but downstream executors fail to process them in time due to severe under-provisioning.

![Load Test Report Highlighting Squeezed Failure Rates](attachment:Screenshot 2026-07-27 at 5.52.12 PM.png)

* **Target Load**: 40 users
* **Spawn Rate**: 8.00 users/second
* **Throughput**: ~19.63 requests/second arriving at the gateway
* **Failures**: 100% failure rate across 1,170 requests

---

### Conclusion & Next Steps

1. **Network Optimization Alone is Insufficient**: While tuning `somaxconn` and persistent `ConnectionPool` instances prevents TCP socket exhaustion, making the network faster only injects tasks into the Redis broker faster, aggravating the backlog.
2. **Horizontal Scaling is Required**: To match the ingestion rate of high-concurrency traffic, executor worker capacity must scale up to match compute demands (e.g., establishing a higher worker-to-gateway ratio such as 1:6 or scaling executor replicas via Kubernetes).
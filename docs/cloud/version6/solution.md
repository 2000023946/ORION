# Queue-Based Autoscaling & Ingestion Bottleneck Analysis Report

## 1. Overview

This report evaluates the transition from CPU-based Horizontal Pod Autoscaling (HPA) to KEDA-driven queue-depth autoscaling for the **Orion** asynchronous architecture. By comparing terminal telemetry logs and load-testing metrics across both runs, this analysis identifies why the executor remained underutilized and establishes the architectural remediation required to unblock processing capacity.

---

## 2. Telemetry Log Comparison

### Baseline Run: CPU-Based Scaling

In the initial baseline run, the executor relied strictly on native CPU utilization thresholds (`70% target`).

```text
NAME                 REFERENCE                   TARGETS        MINPODS  MAXPODS  REPLICAS  AGE
api-gateway-hpa      Deployment/api-gateway      cpu: 151%/70%  1        2        2         11d
orion-executor-hpa   Deployment/orion-executor   cpu: 75%/70%   1        4        2         10m
...
api-gateway-hpa      Deployment/api-gateway      cpu: 11%/70%   1        2        2         11d
orion-executor-hpa   Deployment/orion-executor   cpu: 13%/70%   1        4        2         16m
api-gateway-hpa      Deployment/api-gateway      cpu: 10%/70%   1        2        1         11d
orion-executor-hpa   Deployment/orion-executor   cpu: 10%/70%   1        4        1         16m
orion-executor-hpa   Deployment/orion-executor   cpu: 25%/70%   1        4        1         17m
orion-executor-hpa   Deployment/orion-executor   cpu: 18%/70%   1        4        1         18m
orion-executor-hpa   Deployment/orion-executor   cpu: 20%/70%   1        4        1         19m

```

* **Observation:** The `api-gateway` CPU spiked to **151%**, hitting its hard limit of `maxReplicas: 2`.
* **Flaw:** The `orion-executor` CPU briefly hit 75%, but quickly dropped down to 10%–25%. The CPU-based autoscaler prematurely scaled the executor down to `1 replica` at the 16-minute mark, remaining blind to the asynchronous workload waiting to be processed.

---

### Secondary Run: KEDA Queue-Based Scaling

To fix autoscaler desynchronization, KEDA was introduced to monitor the Redis queue depth (`10 tasks/pod target`).

```text
NAME                                  REFERENCE                          TARGETS        MINPODS  MAXPODS  REPLICAS  AGE
api-gateway-hpa                       Deployment/api-gateway             cpu: 184%/70%  1        2        2         11d
keda-hpa-orion-executor-scaler        Deployment/orion-executor          0/10 (avg)     1        4        2         15s
...
keda-hpa-orion-executor-scaler        Deployment/orion-executor          0/10 (avg)     1        4        1         5m34s

```

* **Observation:** The `api-gateway` CPU usage worsened, reaching a critical **184%** saturation.
* **Flaw:** KEDA continuously reported `0/10 (avg)` for the `orion-executor`. Because the queue length stayed at zero, KEDA kept the executor replica count low (`1` to `2` pods).

---

## 3. Load Test Results (KEDA Metric Dashboard)

| Metric | 100 Users | 250 Users | 500 Users |
| --- | --- | --- | --- |
| **Average Response Time (ms)** | ~60,000 ms | < 1,000 ms | ~2,000 ms |
| **Throughput (Req/s)** | ~1 req/s | ~12 req/s | ~135 req/s |
| **Failures (Count)** | 0 failures | ~1,500 failures | ~13,700 failures |

### Key Findings:

1. **Initial Latency Spike:** At 100 concurrent users, response times reached 60,000 ms due to initial socket backlog buildup at the ingestion layer.
2. **Artificial Response Time Drop:** At 500 users, response time appears artificially fast (~2,000 ms), but this was caused by **immediate connection drops** at the gateway.
3. **Massive Failure Volume:** Request failures linearly escalated to over **13,700 dropped requests** at 500 users.

---

## 4. Root Cause: API Gateway Ingestion Choking

The logs and metrics confirm that **the executor was not underperforming—it was starving for work.**

1. **Ingestion Bottleneck:** The `api-gateway` deployment was capped at `maxReplicas: 2`. Under 500 concurrent users, connection handling and serialization drove Gateway CPU to **184%**.
2. **Connection Rejection:** Saturated OS socket backlogs caused the Gateway to reject incoming TCP requests outright, returning 502/503 errors back to Locust.
3. **Zero Queue Ingestion:** Because requests were dropped before reaching the Redis message broker, the queue depth remained at `0/10 (avg)`.
4. **Executor Inaction:** KEDA performed as designed: seeing an empty queue, it did not scale up the `orion-executor`. The executor remained idle simply because the Gateway choked before feeding tasks into the pipeline.

---

## 5. Remediation Plan

To allow queue-based autoscaling to function, the producer layer must be expanded to handle high-concurrency ingestion:

1. **Scale API Gateway Capacity:** Increase `api-gateway` `maxReplicas` from **2 to 4** (or higher). This provides the CPU headroom necessary to ingest burst traffic, handle TCP connections, and populate Redis.
2. **Retain KEDA Scaling:** Maintain `keda-hpa-orion-executor-scaler` on the consumer layer. Once the Gateway successfully routes payloads into Redis, KEDA will detect the queue depth increase and scale the executor pods proactively.
## Baseline Load Test Report: Single-Worker Bottleneck

### Executive Summary

The system architecture in its current static configuration cannot sustain a throughput of **1 Request Per Second (RPS)**. The backend worker processing time (~3 seconds per task) creates a severe structural bottleneck. When incoming traffic exceeds the single worker's maximum theoretical throughput of ~0.33 RPS, tasks accumulate in the Redis message broker, causing severe cascading latency and system-wide connection timeouts within seconds.

### Test Methodology

* **Target:** FastAPI Gateway routing to a Redis message bus (`queue:search_tasks`), processed by a static worker (TEI / Qdrant).
* **Load Profile:** Stepped RPS intervals (1, 2, 4, 8, 16), sustained for 90 seconds each.
* **Timeout Threshold:** 10 seconds per HTTP request.

### Performance Metrics

The test was effectively halted at 2 RPS due to a total system stall, rendering the higher RPS tiers irrelevant until the architecture is scaled.

| Metric | 1 RPS Phase (90s) | 2 RPS Phase (90s) |
| --- | --- | --- |
| **Total Requests Fired** | 90 | 179 |
| **Success Rate** | 5.6% | 0.0% (Total Failure) |
| **Average Latency** | 6068.0 ms | N/A (100% Timeouts) |
| **Peak Queue Depth** | 49 tasks | 49 tasks |

### Root Cause Analysis

1. **Processing Deficit:** A single request requires approximately 3 seconds to generate vector embeddings and query the database. At 1 RPS, the system receives 3 requests in the time it takes to process 1.
2. **Queue Saturation:** Because the ingestion rate (API Gateway) outpaces the consumption rate (Worker Pod), unhandled tasks stack in the Redis `queue:search_tasks` list.
3. **Cascading Timeouts:** By the 6th request of the 1 RPS test, the queue wait time physically exceeded the 10-second HTTP timeout threshold. At 2 RPS, the queue flooded so rapidly that zero requests survived the wait time.

### Strategic Recommendations

To resolve this bottleneck and prepare the architecture for production-level traffic, the system requires a shift from static provisioning to dynamic, event-driven scaling.

* **Implement Horizontal Pod Autoscaling via KEDA:** Standard CPU-based autoscaling is insufficient because the API Gateway absorbs the traffic while the worker CPU remains steady. Deploy KEDA to monitor the `LLEN` of `queue:search_tasks` and dynamically spin up parallel worker pods when the queue depth exceeds a configured threshold (e.g., 3 tasks).
* **Introduce Vector Similarity Edge Caching:** To reduce the base 3-second processing time, introduce an intermediary caching layer. Storing frequently accessed embeddings at the edge will allow the API Gateway to bypass the queue and worker pods entirely for repeated or highly similar queries.
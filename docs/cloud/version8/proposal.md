
## Current Baseline Limits

* **Safe Operating Capacity (0.33 RPS):** The system handles this perfectly. You achieved a **100% success rate** with an average latency of ~3.2 seconds. The Redis queue stays healthy, never exceeding 2 pending tasks.
* **The Breaking Point (0.66 RPS):** The system begins to collapse. The success rate plummets to **20%**, average latency spikes to nearly 6 seconds, and the queue backs up to 22 tasks. Looking at the latency graph, almost all requests are flatlining at exactly 10,000ms, indicating a hard 10-second network timeout.
* **Total Failure (1.0 RPS):** The system is completely overwhelmed. You hit a **0% success rate**, and the Redis queue rapidly climbs to 45 pending tasks.

## What This Data Tells Us

The `asyncio` worker refactor worked exactly as expected — it is successfully pulling multiple tasks off the Redis queue and firing them concurrently. However, this load test confirms the operational risk we discussed earlier: **Downstream Saturation**.

Because your worker is no longer rate-limiting itself by waiting sequentially, it is slamming the external API (TEI/Qdrant) with too many concurrent connections at once. At 0.66 RPS and above, the downstream service simply cannot compute the queries fast enough for the volume of simultaneous requests it is receiving. The requests sit open, hit their 10-second timeouts, and fail, while the Redis queue continues to fill up.

## The Path Forward

To push past 0.33 RPS, we cannot just push a single worker harder. We need to protect the downstream API while increasing our processing power:

1. **Pod-Level Concurrency Limits:** We need to add an `asyncio.Semaphore` to your Python worker. This will act as a safety valve, capping the maximum number of concurrent HTTP requests a single pod can send at any given time, preventing it from crashing the downstream services.
2. **Horizontal Autoscaling:** With the semaphore protecting the downstream API, we can safely scale the *number* of pods. Integrating KEDA for queue-depth-based horizontal autoscaling will allow the cluster to dynamically spin up additional worker pods when the Redis queue starts to back up.
3. **Traffic Reduction:** Implementing vector similarity edge caching will help intercept repeat queries, serving them instantly and reducing the total load that reaches the backend workers in the first place.
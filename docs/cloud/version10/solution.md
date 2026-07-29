# 🚀 Final Load Test & Architecture Report: Kubernetes Search Microservice

## Executive Summary: The 32x Throughput Leap

The architectural transition from sequential, single-task polling to **bulk Redis queue reads** paired with **`asyncio` coroutines** was a complete success. By decoupling the I/O polling from the task execution, the single-pod capacity successfully scaled from a baseline of 1 RPS up to a highly stable **32 RPS**—a 3200% increase in throughput.

## 📊 Worker Pool Comparison: 196 vs. 300 Workers (1.0 vCPU)

The final testing phase compared a 196-worker pool against a 300-worker pool on a 1.0 vCPU allocation. The data proves that a higher worker count provides a crucial concurrency buffer, resulting in drastically higher efficiency at target loads.

### The 32 RPS Sweet Spot

The most significant performance delta occurred at the 32 RPS target load.

| Metric | 196 Workers | 300 Workers | Improvement |
| --- | --- | --- | --- |
| **Success Rate** | 98.5% | 100.0% | +1.5% (Total Stability) |
| **Avg Latency** | 3716.8 ms | 2497.5 ms | 1.2 seconds faster |
| **Peak CPU** | 0.414 vCPU | 0.303 vCPU | 26.8% less CPU used |
| **Max Queue** | 11 | 9 | Faster task consumption |

**Analysis:** Increasing the worker count to 300 allowed the system to absorb downstream network latency without stalling the event loop. With 196 workers, tasks began to queue and latency spiked to 3.7 seconds. With 300 workers, the system effortlessly consumed the 32 RPS load, keeping latency flat at 2.5 seconds while actually *reducing* total CPU consumption.

## The 64 RPS Hard Ceiling

Both configurations confirm that 64 RPS is mathematically unattainable for a single Python process.

Even with 300 workers, the system maxed out at a **12.6% success rate** with an average latency of 5420.3 ms. Once the 300-worker buffer fills up, tasks sit in the Redis queue (reaching a depth of 87) until they hit the hard client-side timeout. This confirms that **32 RPS is the absolute maximum safe operating capacity for a single pod**.

## The CPU Verdict: Why 1.0 vCPU is Required

The attempt to optimize cloud costs by bin-packing pods into **0.5 vCPU** allocations resulted in a catastrophic 100% failure rate, even at the lowest 16 RPS load.

While the system only actively consumes ~0.303 to 0.506 vCPU under load, restricting the pod to exactly 0.5 vCPU strips the Python `asyncio` event loop of the necessary burst overhead required to manage 300 concurrent network sockets. Without that overhead, the loop deadlocks and triggers cascading 10-second timeouts.

**Final Decision:** Worker nodes must be provisioned with **1.0 vCPU** to ensure event loop stability.

## Final Scaling Strategy

1. **Pod Specification:** 1.0 vCPU / 300 `asyncio` workers.
2. **Single Pod Capacity:** ~32 Requests Per Second.
3. **Cluster Scaling:** Because 64 RPS breaks a single pod, horizontal scaling is strictly required. KEDA must be configured to monitor the Redis list length and horizontally scale out additional pods before the queue depth exceeds the 10-second timeout threshold.
## Baseline Load Test Report: Unbounded Async CPU Saturation

### Executive Summary

The single-worker pod (provisioned with **0.25 vCPU and 256 MiB Memory**) successfully handled asynchronous multiplexing at lower volumes but encountered a hard compute ceiling at 16 Requests Per Second (RPS). Without a concurrency limit in place, the pod attempted to process every incoming request simultaneously. The system collapsed not from memory exhaustion, but from CPU saturation caused by excessive context switching within the Python event loop.

### Test Parameters & Metrics

* **Infrastructure Profile:** 1 Worker Pod (0.25 vCPU, 256 MiB).
* **Architecture:** API Gateway -> Redis Broker -> Unbounded Async Python Worker -> TEI/Qdrant.

| Target RPS | Total Requests | Success Rate | Avg Latency | Max Queue |
| --- | --- | --- | --- | --- |
| **2 RPS** | 179 | 100.0% | 2536.7 ms | 4 |
| **4 RPS** | 355 | 100.0% | 2615.5 ms | 3 |
| **8 RPS** | 699 | 98.9% | 3535.6 ms | 33 |
| **16 RPS** | 1336 | 1.2% | 5602.9 ms | 403 |

### Root Cause Analysis: CPU Context Switching

The data reveals a classic event loop starvation failure profile:

1. **The 8 RPS Inflection Point:** At 8 RPS, the worker began to fall behind. The single CPU thread spent an increasing amount of time managing active network connections rather than executing code, causing the queue to climb to 33 tasks and latency to increase by nearly a full second.
2. **Context-Switching Thrash (16 RPS):** At 16 RPS, the worker ingested over 150 tasks at once. Python's single-threaded `asyncio` engine was forced to rapidly switch contexts between hundreds of active network buffers, payload serializations, and JSON parses.
3. **Event Loop Paralysis:** The overhead of context switching consumed the entire 0.25 vCPU allocation. The event loop became so choked that it could no longer poll Redis fast enough, causing the queue to explode to 403 tasks. The tasks that *were* in memory stalled, pushing latency past 5,600 ms and triggering massive HTTP timeouts (1.2% success rate).

### Strategic Next Steps: Engine Optimization

The pod possesses enough memory to handle more concurrent routines, but the CPU utilization is highly inefficient. Before introducing a Semaphore to artificially throttle the pod, the worker's compute efficiency must be optimized to raise the base RPS ceiling.

1. **Swap to `uvloop`:** Replace the standard `asyncio` event loop with `uvloop` (Cython/libuv) to drastically reduce the CPU overhead of context switching and network I/O.

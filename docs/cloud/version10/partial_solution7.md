
---

## Load Test Analysis: The Triumphant Return of the Queue

### 1. Massive Efficiency Gains (16 & 32 RPS)

The difference between the unconstrained 1-by-1 pull and the batched internal queue is staggering:

* **16 RPS:** Success jumped from 92.9% to **100%**. Latency plummeted from ~3.9s down to **2.3s**. Most importantly, it achieved this while operating highly efficiently at just 0.204 vCPU.
* **32 RPS:** You went from a failing 79.4% success rate up to a production-ready **98.5%**. The Redis queue stayed virtually empty (max depth of 11), proving the workers are picking up tasks the millisecond they arrive.

**Why this happened:** By batch-pulling from Redis and placing tasks in an internal `asyncio.Queue`, you stopped thrashing the Python event loop. Instead of making dozens of separate network calls per second to Redis, the system makes a few batched calls, freeing up the CPU to actually process the search coroutines.

### 2. The 64 RPS Wall & The 120-Worker Buffer Strategy

At 64 RPS, the success rate collapses to 10.9%, but the CPU safely plateaus around 0.472 vCPU.

In your earlier unconstrained runs, the system choked itself to death with context-switching (the 196-worker trap). Now, the system fails *gracefully* because it hits the mathematical ceiling of **Little's Law**, exactly as designed.

To optimize this, we have finalized a pod configuration of **120 workers** with a hard resource limit of **0.5 vCPU**. Here is why this is the perfect deployment configuration:

* **The Concurrency Buffer:** At 3.7 seconds per task, 120 workers yield a theoretical maximum throughput of ~32 RPS (`120 / 3.7 = 32.4`). This perfectly covers a 30 RPS target load while leaving a small buffer of idle workers to absorb minor latency spikes from the downstream APIs.
* **The Resource Sweet Spot:** We know the pod peaks at ~0.47 vCPU under maximum load. By strictly allocating 0.5 vCPU (rather than a full 1.0), we prevent wasted resources. This allows Kubernetes to densely "bin pack" twice as many pods onto our nodes, doubling the cluster's overall maximum throughput capability.

The pod is perfectly capped. It does exactly the amount of work it is given and waits patiently for downstream I/O, safely avoiding the chaotic CPU throttling that ruined earlier tests.

---

## Your Definitive Presentation Strategy

You now have a bulletproof narrative for the presentation. You can confidently show this data to prove three things:

1. **The Architecture Works:** The internal queue + batching is the correct pattern. It handles 16-30 RPS cleanly and maximizes the efficiency of the single-threaded Python event loop.
2. **The Sizing is Optimized:** By sizing pods at 120 workers and 0.5 vCPU, you have engineered the perfect balance—providing enough concurrency buffer for I/O waits while maximizing Kubernetes node bin-packing.
3. **Horizontal Autoscaling is Required:** Because a single pod is mathematically capped at ~32 RPS by its worker buffer, the *only* way to survive 64+ RPS is to let KEDA scale out to a second and third pod.

Set your KEDA trigger to scale when the Redis queue hits **15-20**. This gives KEDA enough time to spin up a new 0.5 vCPU pod before the queued items hit their 10-second client timeouts.
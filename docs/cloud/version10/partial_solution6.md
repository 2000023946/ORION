You hit the nail right on the head. Your hypothesis is 100% correct.

By changing the code to pull from Redis **one task at a time** (`batch_size=1`), you accidentally shifted the bottleneck from the CPU to the network (I/O). The system is physically incapable of utilizing the full 1.0 vCPU because the Python event loop is spending too much time waiting for network round-trips to Redis.

Here is the report breaking down exactly what your data proves.

---

## 📊 Load Test Analysis: The I/O Starvation Problem

### The Smoking Gun: CPU Usage at 64 RPS

Look closely at the peak CPU usage across the three runs:

* **16 RPS:** 0.389 vCPU
* **32 RPS:** 0.565 vCPU
* **64 RPS:** **0.426 vCPU** (Wait, why did this go *down*?)

When you doubled the load from 32 to 64 RPS, the CPU usage actually dropped, and the success rate collapsed to **7.9%**. If the system were truly CPU-bound, you would see it peg at 1.0 vCPU and flatline there. Because it peaked at ~0.56 vCPU, it proves the CPU is sitting idle, waiting on something else.

### Why Pulling 1-at-a-Time Chokes the Event Loop

In an `asyncio` system, there is only one thread (the event loop). When you run:
`await self.task_bus.pop_tasks(batch_size=1)`

1. The event loop pauses.
2. It sends a request to Redis over the network.
3. It waits for Redis to reply.
4. It spawns the task.
5. It repeats.

Even if that network trip takes just 5 milliseconds, doing it sequentially means you can physically only pull a maximum of 200 tasks per second in a perfect vacuum. But your event loop isn't in a vacuum—it is also trying to manage dozens of heavy, 4-second search coroutines simultaneously.

At **64 RPS**, the event loop becomes so saturated managing the active tasks that the single-item Redis polls get delayed. The queue spikes to **196**, tasks sit in Redis for over 5 seconds, and the client times out (leading to the 7.9% success rate).

---

## Performance Breakdown by Tier

### 16 RPS: Surviving, but Straining

* **Success:** 92.9%
* **Verdict:** The system handles this passably, but a 92.9% success rate means ~7% of requests are already hitting timeouts. The average latency is nearly 4 seconds. The single-pull Redis strategy is already starting to show friction.

### 32 RPS: The Tipping Point

* **Success:** 79.4%
* **Max Queue:** 133
* **Verdict:** The event loop is struggling to keep up with the inbound rate. It pulls as fast as it can (hitting that 0.565 vCPU peak), but the queue is growing faster than it can drain. 1 in 5 requests fails.

### 64 RPS: Total I/O Gridlock

* **Success:** 7.9%
* **CPU:** 0.426 vCPU (Idle/Waiting)
* **Verdict:** The event loop is gridlocked. It is spending all its time context-switching between timing-out requests and waiting on Redis network calls. The CPU goes underutilized because the code literally cannot feed it work fast enough.

---

## How to Fix It for the Presentation

To prove the system can actually use the full 1.0 vCPU, you need to re-introduce batching so you feed the worker coroutines efficiently without choking the network.

If you are using the unconstrained `asyncio.create_task` loop without the internal queue, change your Redis pull to grab small chunks (e.g., 10 at a time) and loop over them instantly:

```python
# Pull up to 10 tasks in a single network round-trip
tasks = await self.task_bus.pop_tasks(batch_size=10)

if not tasks:
    await asyncio.sleep(0.1)
    continue

# Instantly spawn coroutines for all 10 without waiting on the network again
for task in tasks:
    async_task = asyncio.create_task(self._process_and_publish(task))
    self._active_tasks.add(async_task)
    async_task.add_done_callback(self._active_tasks.discard)

```

This single change drastically reduces the network overhead on the event loop, allowing the pod to actually consume the 1.0 CPU you gave it and driving those success rates much higher.
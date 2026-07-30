The load test with **96 workers** provides clear visibility into how the system behaves near its hardware ceiling.

Increasing workers to 96 improved handling at 16 RPS, but also revealed why a single pod cannot achieve 32 RPS regardless of worker count.

---

## Benchmarking Comparison: 48 Workers vs. 96 Workers

| Profile | Metric | 48 Workers (`queue_maxsize=100`) | **96 Workers (`queue_maxsize=500`)** | Impact / Delta |
| --- | --- | --- | --- | --- |
| **8 RPS** | Success Rate | 100.0% | **100.0%** | Stable |
|  | Avg Latency | 2536.9 ms | **2464.6 ms** | -72.3 ms |
|  | Peak CPU | 0.103 vCPU | **0.091 vCPU** | -0.012 vCPU |
|  | Max Queue | 10 | **9** | Stable |
| **16 RPS** | Success Rate | 100.0% | **100.0%** | Stable |
|  | Avg Latency | 3075.0 ms | **2963.9 ms** | **-111.1 ms** |
|  | Peak CPU | 0.151 vCPU | **0.165 vCPU** | +0.014 vCPU |
|  | **Max Queue** | **50** | **24** | **-52% lower queue depth** |
| **32 RPS** | Success Rate | 7.7% | **8.5%** | +0.8% |
|  | Avg Latency | 5160.4 ms | **5657.3 ms** | +496.9 ms |
|  | Peak CPU | 0.151 vCPU | **0.210 vCPU** | +0.059 vCPU |
|  | Max Queue | 370 | **77** | Capped by client timeouts |

---

## Key Takeaways from the Data

### 1. 16 RPS Is Sweeter & Faster

At 16 RPS, doubling the worker pool from 48 to 96 meant tasks were picked up almost immediately upon arrival in the internal queue:

* **Max Queue cut in half:** Dropped from **50 down to 24**.
* **Lower Latency:** Average latency dropped under 3 seconds ($2963.9\text{ ms}$).
* **Comfortable CPU:** At $0.165\text{ vCPU}$, the pod uses roughly 66% of its $0.25\text{ vCPU}$ Kubernetes limit, leaving plenty of room to service liveness probes.

---

### 2. The Theoretical vs. Real Capacity Ceiling (Why 32 RPS Still Fails)

On paper, the math suggests:


$$\text{Capacity} = \frac{96\text{ workers}}{3.0\text{ seconds}} = 32\text{ RPS}$$

In reality, running 96 concurrent I/O coroutines on a single core ($0.25\text{ vCPU}$) creates scheduling and network buffer contention. Notice how average latency jumped from $2.4\text{s}$ at 8 RPS to **$5.6\text{s}$ at 32 RPS**.

Recalculating effective throughput with the real latency under load:


$$\text{Real Capacity} = \frac{96\text{ workers}}{5.657\text{ seconds}} = 16.97\text{ RPS}$$

Because true pod throughput degrades to **~17 RPS** under heavy concurrent load, sending 32 RPS creates a continuous $15\text{ RPS}$ deficit. Tasks back up in the queue, sit past the 10-second client timeout window, and fail.

---

### 3. Why Max Queue Stapped at 77 (Instead of 500)

Even though `queue_maxsize` was set to 500, the queue never exceeded 77 items.

At a processing rate of ~17 RPS, an item at position 70 in the queue sits waiting for ~4.1 seconds before a worker picks it up. Add the 5.6-second execution time, and total end-to-end latency reaches **$9.7\text{ seconds}$**—right at the 10-second client timeout threshold. Any task deeper than position ~75 times out on the client side before it can finish, preventing the queue from growing any larger.

---

## Recommended Production Baseline

1. **Keep `max_workers = 96`:** It handles 0–16 RPS cleanly, reduces latency, and keeps queue depth minimal.
2. **Cap `queue_maxsize = 150`:** Setting it to 500 does not help because tasks past position ~100 are doomed to time out anyway.
3. **Horizontal Pod Autoscaling Rule:** Set your scaling rule to add a second pod whenever sustained traffic exceeds **16 RPS** or average Redis queue depth exceeds **20**.
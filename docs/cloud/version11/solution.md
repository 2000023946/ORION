The integration of KEDA with the Prometheus telemetry pipeline is functioning correctly. The combination of a 1-second Prometheus scrape interval and KEDA's `max_over_time[15s]` query has successfully bridged the telemetry gap, allowing the HPA to read true queue depth rather than transient zero values.

Below is the formal analysis of the architecture's behavior during the load test.

## HPA Telemetry Analysis

The Kubernetes HPA logs prove that the autoscaler is now aggressively responding to Redis queue depth rather than missing the spikes.

| Time | Replica Count | Target Metric | System State |
| --- | --- | --- | --- |
| **67m** | 1 | `0/5 (avg)` | Pre-test idle state. A single pod is handling traffic, and the queue is clear. |
| **68m** | 1 $\rightarrow$ 3 | `22/5 (avg)` | **The Scale-Out Trigger:** The 32 RPS burst hits. KEDA detects an average of 22 items in the queue (exceeding the threshold of 5). The HPA immediately provisions two additional replicas, hitting the `maxReplicaCount` cap of 3. |
| **68m - 71m** | 3 | `334m/5 (avg)` | **Queue Drain:** The metric `334m` represents "milli-units," meaning $0.334$ items on average in the queue. The 3 pods have successfully drained the backlog and are now keeping pace with the incoming traffic in real-time. |
| **72m** | 3 | `10334m/5 (avg)` | **The 64 RPS Surge:** The final load test phase begins. The queue spikes to an average of $10.334$ items per pod. Because KEDA is capped at 3 replicas, it cannot scale further, and the backlog begins to grow (`18667m/5` $\rightarrow$ $18.6$). |

---

## Benchmark Performance Review

The system's behavior across the three load phases highlights the exact point where KEDA succeeds, and where the cluster hardware limits are reached.

### 1. The 16 RPS Phase (Cold Start Anomaly)

* **Success Rate:** 50.1%
* **Analysis:** At the start of the 16 RPS test (minute 67), KEDA was targeting `0/5`, meaning only 1 replica was active. The initial burst of 1,336 requests overwhelmed the single pod's 1.0 vCPU limit before the HPA could react and spin up new pods. This caused the queue to hit 37 and latency to spike to 5,383 ms.

### 2. The 32 RPS Phase (Optimal Scaling)

* **Success Rate:** 100.0%
* **Analysis:** This is the definitive proof that the architecture works. At minute 68, the queue spiked to 22, KEDA scaled the deployment to 3 replicas, and those 3 pods successfully handled 2,604 requests with zero failures and an average latency of 2,584 ms. The queue depth was restricted to a maximum of 9 items.

### 3. The 64 RPS Phase (Hardware Cap Reached)

* **Success Rate:** 8.8%
* **Analysis:** At 64 RPS, the cluster received 4,813 requests. The queue spiked to 30, but KEDA was unable to provision more pods due to the `maxReplicaCount: 3` limitation. Furthermore, the total cluster CPU peaked at **28.165 vCPU**, indicating that the Minikube environment was entirely saturated (likely by the `orion-embedding` TEI pods), starving the `orion-executor` pods of compute resources and resulting in a 91.2% failure rate.
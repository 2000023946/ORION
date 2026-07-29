## Architecture Rationale: Proactive Queue-Based Autoscaling with KEDA

**Configuration Update:**
Based on our architectural constraints, the KEDA `ScaledObject` `pollingInterval` has been officially reduced to **3 seconds**. This ensures the scaling controller detects queue spikes and provisions new pods well before the hard 10-second client-side timeout can trigger.

Here is the architectural justification and performance projection for utilizing KEDA metric-based scaling in our upcoming load test.

---

### The Strategy: Scaling Ahead of the Load

Our `asyncio` microservice is highly **I/O-bound**, meaning the event loop spends the vast majority of its time waiting on network connections and Redis reads. Because of this, traditional trailing indicators like CPU or memory utilization do not accurately reflect system stress. By the time hardware metrics indicate a problem, the application is already overwhelmed and dropping requests.

We explicitly selected KEDA to enable **preemptive scaling**. By monitoring the actual operational bottleneck—`sum(orion_queue_depth)`—we can scale the system *before* the incoming request load translates into latency and timeouts.

### Why Queue Depth is the Ultimate Leading Indicator

Instead of waiting for the system to choke, KEDA uses the queue as an early warning system:

1. **Direct Correlation to Latency:** The queue depth is the exact predictor of our 10-second timeout. If the queue breaches our threshold of 10, we know the 300 workers are reaching saturation and latency is imminent.
2. **Rapid Reaction Time:** By polling Prometheus every 3 seconds, KEDA catches surges instantly, reacting to the data at the gate rather than the stress on the server.
3. **Mathematical Precision:** At 40+ RPS, the queue will instantly spike above the threshold. KEDA immediately performs the math (`Queue Depth / 10`) and requests 2 to 3 pods, proactively expanding capacity before the backlog hits the 10-second death window.

### Official Performance Projection

When executing the 64 RPS test on local Minikube (allowing up to 3 replicas):

Within 3 to 6 seconds of initiating the 64 RPS load, KEDA will detect the initial queue accumulation. It will immediately provision Pod 2, and likely Pod 3 shortly after. By preemptively distributing the workload across multiple Redis workers *before* the system is fully saturated, the individual queue depths will remain low, preventing timeouts and allowing the system to achieve a **>95% success rate**.
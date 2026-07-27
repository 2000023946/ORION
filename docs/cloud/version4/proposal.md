
---

# Architecture Report: Version 4

## Asynchronous Queue-Based Load Leveling and Decoupled Execution

### Objective

This architecture transition introduces an asynchronous, queue-based execution model to improve system resilience under unpredictable traffic spikes. The objective is to decouple request ingestion from processing workloads, reduce request loss during scaling delays, and prevent excessive load on downstream external services.

---

## 1. Bottleneck Analysis and Queue-Based Load Management

Previous load tests demonstrated that sudden increases in concurrent users can exceed the response time of Kubernetes Horizontal Pod Autoscaling (HPA). During rapid traffic growth, additional worker instances may not become available before existing workers reach capacity, causing increased latency and request failures.

To address this limitation, a message broker layer is introduced using technologies such as Redis Streams, AWS SQS, or RabbitMQ.

The queue provides a buffering mechanism between incoming requests and processing workers:

* The API Gateway can rapidly accept incoming requests and store them in the queue.
* Worker services process queued requests at a controlled rate.
* The infrastructure can scale worker capacity without blocking client requests.
* External APIs are protected from uncontrolled request bursts.

---

## 2. Version 4 System Architecture

The processing pipeline transitions from synchronous service communication to an asynchronous publish/subscribe architecture.

```text
[Client] ──> [API Gateway] ──> [Task Queue (Redis/SQS)]
                                         │
                             ┌───────────┴───────────┐
                             │   Search Worker Pool  │
                             │  (KEDA Autoscaled)    │
                             └───────────┬───────────┘
                                         │
                         [Result Pub/Sub (Request ID)]
                                         │
                             [Core Engine / Gateway]
                                         │
                                      [Client]
```

### Execution Flow

1. **Request Ingestion**
   The API Gateway receives a client request, generates a unique `Request_ID`, stores the task in the queue, and immediately releases processing resources.

2. **Queue Buffering**
   The message broker temporarily stores requests until worker capacity becomes available.

3. **Worker Processing**
   Search workers retrieve queued tasks and execute processing workloads while enforcing concurrency limits for external dependencies.

4. **Result Publishing**
   Completed results are published to a result channel associated with the original `Request_ID`.

5. **Response Delivery**
   The gateway retrieves the corresponding result and returns the completed response to the client.

---

## 3. Operational Requirements

### Event-Driven Autoscaling

CPU-based Horizontal Pod Autoscaling is insufficient for burst-oriented workloads because CPU utilization increases only after workers are already under pressure.

Kubernetes Event-driven Autoscaling (KEDA) enables scaling based on queue metrics, allowing worker instances to increase as queue depth grows.

### Concurrency Control

Worker services must implement internal concurrency limits to prevent excessive external API requests. Asynchronous semaphores can restrict the number of simultaneous external operations and maintain compliance with provider rate limits.

Example:

```python
asyncio.Semaphore(10)
```

### Queue Limits and Backpressure

The queue must implement bounded capacity and request expiration policies.

Required controls include:

* Maximum queue depth limits
* Request TTL enforcement
* Client timeout handling
* Graceful rejection using HTTP responses such as `429 Too Many Requests` or `503 Service Unavailable`

These mechanisms prevent uncontrolled queue growth and maintain system stability during extreme traffic conditions.

---

## Conclusion

Version 4 introduces a fault-tolerant, event-driven architecture by separating request ingestion from workload execution. By using asynchronous queues, controlled worker concurrency, and queue-based autoscaling, the system can absorb traffic spikes while maintaining predictable resource utilization and protecting downstream services from overload.

---


I would structure the entire project like a research experiment. The key principle is:

> **Only split a component into a microservice if the measurements justify it.**

---

# Orion Microservice Evaluation Plan

## Phase 0 — Build a Controlled Monolith

### Goal

Create a stable system that produces repeatable benchmark results.

### Tasks

* Build Orion as a single monolithic application.
* Replace external services with mock implementations:

  * Mock LLM API
  * Mock Web Search API
* Mock APIs should:

  * Sleep for configurable delays
  * Return realistic JSON responses
  * Never call the internet

At this point the architecture is:

```text
Monolith
├── API
├── Graph Executor
├── Planner
├── Vector Search
├── Redis
├── Mock LLM
└── Mock Web Search
```

---

# Phase 1 — Add Instrumentation

### Goal

Measure where every request spends its time.

Instrument every major component.

Record for every request:

* Start time
* End time
* Duration

Optionally record:

* Memory usage (before/after)

Example output:

| Component       | Avg Time | Memory |
| --------------- | -------: | -----: |
| API             |     4 ms |  30 MB |
| Graph Executor  |    28 ms | 120 MB |
| Planner         |    18 ms |  45 MB |
| Vector Search   |   110 ms | 3.8 GB |
| Redis           |     2 ms | 150 MB |
| Mock LLM        |   300 ms |  20 MB |
| Mock Web Search |   520 ms |  15 MB |

---

# Phase 2 — Establish the Baseline

Run Locust against the monolith.

Test:

* 10 users
* 50 users
* 100 users
* 250 users
* 500 users
* 1000 users

Collect:

* Requests/sec
* Average latency
* p95 latency
* Failure rate
* Component timings
* Memory measurements

**Save these results permanently.**

This is the **baseline**.

Never overwrite it.

---

# Phase 3 — Evaluate Each Candidate Independently

Always start from the **original monolith**.

Do **not** build on previous experiments.

---

## Experiment A

Split only:

```text
Graph Executor
```

Run the exact same Locust tests.

Compare with the baseline.

Decision:

* Better → Keep as a candidate.
* Worse → Reject.

Return to the original monolith.

---

## Experiment B

Split only:

```text
Planner
```

Run benchmarks.

Compare with the baseline.

Return to the original monolith.

---

## Experiment C

Split only:

```text
Vector Search
```

Run benchmarks.

Compare with the baseline.

Return to the original monolith.

---

## Experiment D

Split only:

```text
LLM
```

Run benchmarks.

Compare with the baseline.

Return to the original monolith.

---

## Experiment E

Split only:

```text
Web Search
```

Run benchmarks.

Compare with the baseline.

Return to the original monolith.

---

# Phase 4 — Build the Final Architecture

Suppose the experiments show:

| Service        | Improvement | Decision |
| -------------- | ----------- | -------- |
| Graph Executor | ✅           | Split    |
| Planner        | ❌           | Keep     |
| Vector Search  | ✅           | Split    |
| LLM            | ✅           | Split    |
| Web Search     | ❌           | Keep     |

Now construct the final system using only the services that demonstrated a benefit.

---

# Phase 5 — Final Validation

Benchmark the final architecture using the **same Locust workloads**.

Compare:

| Metric            | Monolith | Final Architecture |
| ----------------- | -------: | -----------------: |
| Throughput        |          |                    |
| Avg Latency       |          |                    |
| p95 Latency       |          |                    |
| Failure Rate      |          |                    |
| Component Timings |          |                    |

This answers the most important question:

> **Does the final architecture outperform the original monolith?**

---

# Phase 6 — Analyze the Results

For every component, provide an evidence-based conclusion.

Example:

| Component      | Evidence                                     | Decision         |
| -------------- | -------------------------------------------- | ---------------- |
| Graph Executor | Throughput increased by 32%                  | Microservice     |
| Planner        | No measurable improvement                    | Keep in monolith |
| Vector Search  | Lower latency and isolated memory usage      | Microservice     |
| LLM            | External dependency with high latency        | Microservice     |
| Web Search     | No measurable benefit in this implementation | Keep in monolith |

---

# Final Deliverables

Your report should include:

* **Architecture diagrams**

  * Original monolith
  * Each experimental configuration (optional, simplified)
  * Final microservice architecture
* **Instrumentation results**

  * Per-component timing
  * Optional memory usage
* **Locust benchmark results**

  * Throughput
  * Average latency
  * p95 latency
  * Failure rate
* **Comparison tables**

  * Baseline vs. each experiment
  * Baseline vs. final architecture
* **Evidence-backed architectural decisions**

  * Explain *why* each service was kept in the monolith or extracted into a microservice using your measurements, not general microservice principles.

This gives you a rigorous methodology that is easy to execute, repeatable, and strong enough to defend in a cloud or distributed systems report.

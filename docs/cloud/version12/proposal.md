# Technical Proposal: Semantic Edge Caching for Orion

**Author:** Orion System Architecture Team

**Date:** July 2026

**Status:** Proposed

**Target Subsystem:** Gateway API / Edge Infrastructure (`src/infrastructure/real/cache/`)

---

## 1. Executive Summary

We propose upgrading the Orion API Gateway edge caching layer from **Exact-String Key Hashing (Redis)** to **Semantic Edge Caching (Qdrant + TEI)**.

Currently, cache hits require an identical, byte-for-byte query string match. By replacing exact hashing with vector similarity search against our existing Qdrant and `orion-embedding` (Text Embeddings Inference) instances, we can match queries based on **intent and semantic meaning**.

### Key Objective

Increase edge cache recall and hit rate from **~10–15% to 40–60%+** on recurring user intent patterns, lowering P95 edge response latency to **15–25ms** for cached queries and offloading significant compute from downstream `orion-executor` pods and toolchains.

---

## 2. Problem Statement

Our current caching mechanism (`RedisCacheAdapter`) uses SHA-256 hashing on normalized query strings:

$$\text{Key} = \text{SHA256}(\text{lower}(\text{trim}(Q)))$$

While $O(1)$ fast, exact-string matching introduces significant operational inefficiencies under real-world traffic:

* **Zero Semantic Recall:** Queries like *"How do I scale KEDA pods?"* and *"What is the process for scaling KEDA worker pods?"* produce completely distinct hashes, forcing two full executions through the queue, tool executors, and LLMs.
* **Redundant Pipeline Load:** Downstream microservices (`orion-executor`) waste CPU cycles, vector lookups, and external LLM tokens computing identical answers for slight rephrasings.
* **KEDA Volatility:** Uncached rephrased queries trigger unnecessary Redis queue depth spikes, causing KEDA to aggressively scale up worker pods for queries whose answers are already known.

---

## 3. Proposed Solution: Vector-Based Semantic Cache

We will deploy a `QdrantCacheAdapter` that implements our existing abstract `CachePort` interface without changing any business or API routing logic.

```
Incoming Request
       │
       ▼
[ Fast Embedding ] (orion-embedding / TEI) ──► Vector: [0.024, -0.119, ...]
       │
       ▼
[ Qdrant ANN Search ] (semantic_cache collection)
       │
       ├── Cosine Similarity ≥ 0.92 ──► [ CACHE HIT ]  ──► Return Payload (~15–25 ms)
       │
       └── Cosine Similarity < 0.92 ──► [ CACHE MISS ] ──► Push to Task Bus (Redis Queue)
                                                                    │
                                                                    ▼
                                                           [ Execute Pipeline ]
                                                                    │
                                                                    ▼
                                                           [ Async Upsert to Qdrant ]

```

### Technical Workflow

1. **Embedding Generation:** The Gateway passes incoming query text to the `orion-embedding` container (`all-MiniLM-L6-v2`) to retrieve a 384-dimensional dense vector in ~8–12ms.
2. **Nearest-Neighbor Lookup:** The vector is queried against a dedicated `semantic_cache` collection in Qdrant using Cosine Distance:

$$\text{Similarity}(\vec{q}_{\text{new}}, \vec{q}_{\text{cached}}) = \frac{\vec{q}_{\text{new}} \cdot \vec{q}_{\text{cached}}}{\Vert{}\vec{q}_{\text{new}}\Vert{} \Vert{}\vec{q}_{\text{cached}}\Vert{}}$$

3. **Gated Evaluation:**
* **Score $\ge 0.92$ (Hit):** The cached `SearchTaskResponse` payload is reconstructed and returned immediately with `metadata.gateway_cached = True`.
* **Score $< 0.92$ (Miss):** The task is pushed to the Redis bus for standard DAG execution.


4. **Asynchronous Population:** Upon task completion, `set_answer` writes the vector, original query text, and response payload to Qdrant asynchronously using a deterministic UUID (`uuid5`) derived from the query string to prevent duplicate point creation.

---

## 4. Expected Impact & Metrics

| Metric | Current (Exact Hash Cache) | Proposed (Semantic Cache) | Project Impact |
| --- | --- | --- | --- |
| **Edge Cache Hit Rate** | ~10–15% | **40–60%+** | **3–4x improvement** in edge cache recall |
| **Cached P95 Latency** | ~2ms | **15–25ms** | Sub-30ms responses for all semantically equivalent queries |
| **Uncached P95 Latency** | 1,500ms – 8,000ms+ | Unchanged | N/A |
| **Downstream Pod Compute** | Linear with request volume | **Dramatically Reduced** | Bypasses queue, executor, and LLM calls for hits |
| **Infra Overheads** | None | Low | Reuses running Qdrant + TEI containers; 0 new services |

---

## 5. Architectural & Implementation Plan

### Minimal Footprint Migration

Because the architecture strictly decouples ports and adapters via `CachePort`, the migration requires **zero changes** to `main.py`, domain models (`SearchTaskResponse`, `Query`), or routing logic.

* **New File:** `src/infrastructure/real/cache/qdrant_cache_adapter.py`
* **Updated File:** `src/components/cache_infrastructure.py` (instantiates `AsyncQdrantClient` instead of `Redis` connection pool)

### Cache Eviction & Memory Management

Unlike Redis, vector databases do not natively support key-level TTLs. To maintain Qdrant memory stability:

* Every cached point stores a `created_at` timestamp in its payload.
* A lightweight Kubernetes `CronJob` will run off-peak to delete points older than 24–48 hours using Qdrant's payload filtering API.

---

## 6. Risks & Mitigations

* **Risk 1: False Positives (Incorrect Hits)**
* *Mitigation:* We set an initial conservative similarity threshold of **$\tau = 0.92$**. We can tune this threshold dynamically via environment variables (`SEMANTIC_CACHE_THRESHOLD`) based on initial rollout observations.


* **Risk 2: Embedding Service Latency Overhead**
* *Mitigation:* The `orion-embedding` TEI container runs optimized ONNX runtime inference, returning embeddings in ~8–12ms. Even on a cache miss, the 10ms penalty is negligible compared to the multi-second executor pipeline.


* **Risk 3: Cold Start / Initial Collection Creation**
* *Mitigation:* The `QdrantCacheAdapter` includes lazy collection initialization (`_ensure_collection`), verifying or creating the `semantic_cache` collection upon first request without requiring manual database migrations.



---

## 7. Recommendation & Next Steps

We recommend proceeding with the deployment of `QdrantCacheAdapter`. Testing can be validated during our load testing cycles by firing varied rephrasings of benchmark queries to verify edge hit rates in Grafana.
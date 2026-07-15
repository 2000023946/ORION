
---

# Orion Architecture v2: Solving the 3.15GB Monolith

### The Problem (v1)

In version 1, the gRPC Executor microservice suffered from extreme container bloat, sitting at **3.15 GB**. This was caused by tightly coupling heavy machine learning dependencies (PyTorch, Sentence Transformers) and in-memory vector indexing (FAISS) directly inside the execution routing logic.

This resulted in:

* **Massive Cold Starts:** Kubernetes Horizontal Pod Autoscaler (HPA) took minutes to pull the image and boot new pods during traffic spikes.
* **OOM Risks:** FAISS stored all vectors in RAM, risking Out-Of-Memory crashes at enterprise scale.

### The Solution (v2)

We transitioned to a true distributed microservice architecture by decoupling the heavy ML workloads from the execution logic.

#### 1. Externalized Embedding Engine

Removed internal PyTorch and Sentence Transformer dependencies. We now use the official **Hugging Face Text Embeddings Inference (TEI)** container (`ghcr.io/huggingface/text-embeddings-inference:cpu-latest`).

* *Benefit:* Rust-backed, lightning-fast token batching with zero model-graph compilation.


#### 3. The Slim Executor

The custom gRPC Executor now solely handles API routing and graph execution logic, utilizing standard HTTP/gRPC adapters to communicate with the ML services.

### The Result

The gRPC Executor image was reduced from **3.15 GB to ~180 MB (a ~94% reduction)**.

New Executor pods now boot in seconds, enabling true, instantaneous horizontal scaling in Kubernetes.
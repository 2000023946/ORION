### Proposal: Decoupling ML Embeddings from the Graph Executor

This proposal outlines the architectural shift from a monolithic executor to a decoupled microservice pattern (**Pattern A**). By separating the embedding generation from the logical graph execution, we eliminate the $3\text{GB}+$ container size bottleneck and unlock sub-second Kubernetes autoscaling.

---

### 1. Current State & The 3GB Bottleneck

The current `orion-executor` image stands at **$3.15\text{ GB}$**.

```
[ Local API Gateway ]
        │
        ▼ (gRPC)
[ Orion Executor Container (3.15 GB) ]
   ├── Graph & DAG Engine
   └── Sentence Transformers (PyTorch + Model Weights)

```

#### The Problem:

* **Autoscaling Failures (Cold Starts):** When the Horizontal Pod Autoscaler (HPA) triggers a scale-up event during traffic spikes, Kubernetes must pull a $3.15\text{ GB}$ image over the network. This causes massive container cold starts (minutes of downtime in `ContainerCreating` status) rather than responding in seconds.
* **Wasted Resource Allocation:** Every time a new replica spins up to handle execution routing, we are forced to provision an extra $3\text{ GB}+$ of disk and memory just to run basic logical routing.

---

### 2. Proposed Architecture (Pattern A)

We will extract the Hugging Face `sentence-transformers` library and model weights into their own single-purpose service: the **Orion Embedding Service**.

```
[ Local API Gateway ]
        │
        ▼ (gRPC / Port-Forward)
[ K8s Service: executor-microservice ] ──► [ Pod: Orion Executor (<150MB) ]
                                                  │
                                                  ▼ (Internal HTTP/gRPC)
                                           [ K8s Service: embedding-service ]
                                                  │
                                                  ▼
                                           [ Pod: Embedding Service (3GB) ]

```

* **Orion Executor (<150MB):** Houses only the logical graph execution engine, MongoDB driver, and gRPC server. This image compiles in seconds, has a tiny memory footprint, and scales instantly.
* **Orion Embedding Service (~3GB):** Houses PyTorch, `sentence-transformers`, and the localized model weights. It exposes a simple endpoint (`POST /embed`) to accept raw text strings and return vector coordinates.

---

### 3. Impact Analysis

| Metric | Current Monolithic Executor | Proposed Decoupled Executor |
| --- | --- | --- |
| **Image Size** | $3.15\text{ GB}$ | **$<150\text{ MB}$** |
| **Scale-Up Time (Cold Start)** | $2\text{ to }5\text{ Minutes}$ (Network bound) | **$<3\text{ Seconds}$** |
| **HPA Scaling Rule** | Scales whole $3\text{ GB}$ bundle | Scales the tiny Executor; keeps the 3GB service static |
| **Memory Footprint per Pod** | High ($\ge 1\text{GB}$ baseline) | **Minimal ($<128\text{MB}$ baseline)** |

---

### 4. Implementation Steps

1. **Create the Embedding Microservice:** Pack the embedding execution logic into a lightweight Python API (such as FastAPI or a basic gRPC server) inside `./embedding-service`.
2. **Strip Executor Dependencies:** Remove `sentence-transformers`, `torch`, and heavy ML model downloads from the Executor’s `requirements.txt` and Dockerfile.
3. **Configure Internal Discovery:** Update the Executor to request embeddings from `http://embedding-service:8000/embed` (or gRPC equivalent) when executing vector-dependent steps.
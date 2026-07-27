# Orion Architecture v2: Decoupling Machine Learning Inference from the Execution Engine

## 1. Background

The initial implementation of the Orion execution framework combined graph orchestration, embedding generation, and vector indexing within a single execution service. Although functionally correct, this architecture tightly coupled orchestration logic with computationally intensive machine learning dependencies, resulting in a large deployment artifact and reduced operational scalability.

---

## 2. Initial Architecture

In Version 1, the gRPC Executor contained both the graph execution engine and the complete machine learning inference stack.

```text id="6f0lvg"
                gRPC
API Gateway ─────────────► Orion Executor (3.15 GB)
                               ├── Graph Executor
                               ├── PyTorch
                               ├── Sentence Transformers
                               └── FAISS Vector Index
```

The resulting container image occupied approximately **3.15 GB**.

### Architectural Limitations

This design introduced several operational challenges.

#### Large Container Images

The executor image contained the graph execution engine together with the complete machine learning runtime, including PyTorch, the `sentence-transformers` library, pretrained embedding models, and the FAISS vector index. Consequently, every executor replica carried the full inference stack regardless of whether additional inference capacity was required.

#### Slow Horizontal Scaling

When Kubernetes Horizontal Pod Autoscaling (HPA) provisioned additional executor replicas during periods of increased demand, each replica required downloading and initializing the complete **3.15 GB** container image. This substantially increased pod startup time and delayed the availability of newly scheduled replicas.

#### Memory Consumption

Because FAISS maintained vector indexes in memory, executor instances required a relatively large baseline memory allocation. As dataset sizes increased, memory utilization grew proportionally, increasing the likelihood of resource exhaustion under large-scale workloads.

---

## 3. Revised Architecture

Version 2 separates orchestration from machine learning inference by introducing dedicated inference services while retaining a lightweight execution engine.

```text id="nshgjl"
                    gRPC
API Gateway ─────────────► Orion Executor (~180 MB)
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
     Hugging Face TEI             Vector Database
(Text Embeddings Inference)        (External Storage)
```

Under this architecture, the executor performs orchestration only, while embedding generation and vector storage are delegated to specialized services.

---

## 4. Architectural Changes

### Externalized Embedding Inference

Machine learning inference was removed from the executor and delegated to the official **Hugging Face Text Embeddings Inference (TEI)** service.

The TEI service provides:

* Pretrained embedding model hosting
* Efficient token batching
* Optimized inference execution
* HTTP-based inference endpoints

By relying on a dedicated inference service, the executor no longer requires PyTorch, Sentence Transformers, or locally hosted embedding models.

---

### External Vector Storage

Vector indexing responsibilities were separated from the execution service.

Instead of maintaining an in-memory FAISS index within each executor instance, vector storage is managed independently by the vector database layer.

This architectural separation prevents executor memory utilization from scaling with dataset size and enables storage resources to be managed independently of execution resources.

---

### Lightweight Execution Engine

The revised gRPC Executor now contains only the components required for orchestration.

These responsibilities include:

* Graph execution
* DAG scheduling
* API routing
* gRPC communication
* HTTP client communication
* Retrieval coordination

Machine learning inference and vector indexing are no longer part of the executor runtime.

---

## 5. Architectural Impact

| Metric                            |                                 Version 1 |                                  Version 2 |
| --------------------------------- | ----------------------------------------: | -----------------------------------------: |
| **Executor Image Size**           |                                   3.15 GB |                                **~180 MB** |
| **Image Size Reduction**          |                                         — |                      **Approximately 94%** |
| **Machine Learning Dependencies** |                  Embedded within executor |                Dedicated inference service |
| **Vector Index Storage**          |                               Local FAISS |                   External vector database |
| **Executor Startup Time**         | Limited by large container initialization | Significantly reduced due to smaller image |
| **Horizontal Scaling**            |            Replicates complete ML runtime |        Replicates orchestration layer only |

---

## 6. Operational Benefits

The revised architecture provides several operational advantages.

### Faster Deployment

Reducing the executor image from **3.15 GB** to approximately **180 MB** substantially decreases image transfer and container initialization time, allowing Kubernetes to provision new executor replicas more rapidly during scaling events.

### Independent Service Scaling

Machine learning inference and orchestration can now scale independently according to their respective workloads. Additional executor replicas no longer duplicate the complete machine learning runtime, resulting in more efficient resource utilization.

### Reduced Resource Consumption

Removing PyTorch, Sentence Transformers, and local vector indexes from the executor decreases baseline memory consumption and reduces computational overhead associated with maintaining machine learning dependencies.

### Improved Maintainability

Separating orchestration, inference, and vector storage into independent services simplifies deployment, dependency management, and future system evolution. Each component can be updated, optimized, and scaled independently without affecting the remaining architecture.

---

## 7. Conclusion

The Version 2 architecture transforms the original execution service from a monolithic orchestration and inference engine into a lightweight execution component responsible solely for coordinating retrieval workflows. Machine learning inference is delegated to a dedicated Hugging Face Text Embeddings Inference service, while vector storage is managed independently.

This architectural refactoring reduces the executor image size by approximately **94%**, improves deployment efficiency, enables more responsive horizontal scaling, and establishes a clearer separation of concerns between orchestration, inference, and data management.

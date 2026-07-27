# Architecture Proposal: Decoupling the Embedding Service from the Graph Executor

This proposal presents an architectural modification that separates machine learning inference from the graph execution engine. The proposed design decomposes the current monolithic execution service into two independently deployable microservices, allowing computationally intensive embedding generation to scale independently from orchestration logic. This separation significantly reduces the deployment size of the execution service and improves the responsiveness of Kubernetes Horizontal Pod Autoscaling (HPA).

---

# 1. Current Architecture

The current implementation packages both the graph execution engine and the machine learning embedding model within a single execution container.

```text
[ Local API Gateway ]
        │
        ▼ (gRPC)
[ Orion Executor Container (3.15 GB) ]
   ├── Graph & DAG Engine
   └── Sentence Transformers (PyTorch + Model Weights)
```

The resulting container image has a size of approximately **3.15 GB**.

## Architectural Limitations

The current deployment introduces two primary operational limitations.

### Large Deployment Artifact

The execution service includes both orchestration logic and machine learning dependencies, including the PyTorch runtime, the `sentence-transformers` library, and pretrained model weights. Consequently, every executor replica contains the complete machine learning runtime regardless of whether additional inference capacity is required.

### Slow Horizontal Scaling

During periods of increased demand, Kubernetes Horizontal Pod Autoscaling provisions additional executor replicas. Because each replica requires downloading and initializing a container image exceeding **3 GB**, pod initialization is dominated by image transfer and startup overhead. Newly scheduled pods therefore remain in the `ContainerCreating` state for an extended period before becoming available to process requests.

As a result, the autoscaling mechanism cannot respond rapidly to sudden increases in workload.

---

# 2. Proposed Architecture

The proposed architecture extracts embedding generation into an independent microservice while retaining graph orchestration within a lightweight execution service.

```text
[ Local API Gateway ]
        │
        ▼ (gRPC)
[ Kubernetes Service: executor-microservice ]
                │
                ▼
     [ Orion Executor (<150 MB) ]
                │
                ▼ (Internal HTTP/gRPC)
[ Kubernetes Service: embedding-service ]
                │
                ▼
     [ Embedding Service (~3 GB) ]
```

Under this design, the execution engine becomes responsible solely for orchestration, while embedding generation is delegated to a dedicated inference service.

### Orion Executor

The executor service contains:

* Graph execution engine
* DAG scheduling logic
* MongoDB integration
* gRPC server
* Request orchestration

By removing machine learning dependencies, the executor image is reduced to less than **150 MB**, substantially decreasing deployment time and baseline resource requirements.

### Embedding Service

The embedding service contains:

* PyTorch runtime
* `sentence-transformers`
* Pretrained embedding models
* Vector generation API

The service exposes an internal inference interface that accepts textual input and returns embedding vectors for downstream retrieval operations.

---

# 3. Expected Architectural Impact

| Metric                               |                                               Current Architecture |                                    Proposed Architecture |
| ------------------------------------ | -----------------------------------------------------------------: | -------------------------------------------------------: |
| **Executor Image Size**              |                                                            3.15 GB |                                              **<150 MB** |
| **Container Startup Time**           |                                          Approximately 2–5 minutes |                                  **Less than 3 seconds** |
| **Horizontal Scaling Behavior**      | Entire execution service, including ML dependencies, is replicated | Only the lightweight executor service scales dynamically |
| **Baseline Memory per Executor Pod** |                                         High (approximately ≥1 GB) |                          **Low (approximately <128 MB)** |

Separating inference from orchestration enables Kubernetes to provision new execution replicas significantly faster while maintaining a fixed pool of embedding services that can be scaled independently according to inference demand.

---

# 4. Implementation Strategy

The proposed architectural transition consists of the following stages.

### 4.1 Develop the Embedding Service

Implement a dedicated embedding microservice using an internal communication protocol such as FastAPI or gRPC.

The service should:

* Load pretrained embedding models during startup.
* Accept text inputs through an internal API.
* Return embedding vectors suitable for downstream retrieval.

### 4.2 Remove Machine Learning Dependencies from the Executor

Refactor the execution service by removing:

* `sentence-transformers`
* PyTorch
* Model download logic
* Machine learning runtime dependencies

The executor should retain only orchestration, scheduling, and communication functionality.

### 4.3 Introduce Internal Service Communication

Replace local embedding generation with requests to the dedicated embedding service.

For example, vector generation requests should be directed to an internal endpoint such as:

```text
http://embedding-service:8000/embed
```

or an equivalent gRPC service within the Kubernetes cluster.

---

# 5. Expected Benefits

The proposed architecture separates computational inference from orchestration, allowing each service to scale according to its own workload characteristics. Reducing the executor image from approximately **3.15 GB** to **less than 150 MB** significantly decreases container startup time and improves the responsiveness of Kubernetes Horizontal Pod Autoscaling.

Furthermore, isolating embedding generation into a dedicated service improves modularity, simplifies dependency management, and enables independent optimization of inference infrastructure without affecting the graph execution engine. This separation provides a more maintainable and scalable architecture while preserving the existing orchestration workflow.

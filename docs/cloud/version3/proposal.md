## **Version 3 Proposal: Dedicated Vector Storage Service**

### **Objective**

Transition the FAISS vector index from an embedded, in-memory dependency within the Core Engine to an independent, network-addressable Docker service to support enterprise-scale data volumes.

### **The Architectural Shift: Preventing Memory Exhaustion**

In a production Enterprise Search MCP, the vector database will scale to hold millions of embeddings.

* **The Fatal Flaw of In-Memory:** High-dimensional vectors consume massive amounts of RAM. If FAISS remains embedded in the Core Engine, the engine will quickly exceed its memory limits and be killed by the operating system (OOM kill). Furthermore, it forces a scaling paradox: you cannot horizontally scale your lightweight, stateless orchestration logic without duplicating a massive, multi-gigabyte RAM footprint for every new pod.
* **Proposed State (V3):** The Core Engine treats vector search as an external I/O-bound network call. A dedicated Docker container is provisioned on specialized, memory-optimized infrastructure to hold the massive FAISS index, completely insulating the Core Engine from RAM spikes.

### **Implementation Strategy**

1. **The Wrapper Service:** FAISS will be wrapped in a high-performance, asynchronous web server (FastAPI or gRPC) inside its own Docker image, turning the C++ library into a queryable network database.
2. **Persistent Storage:** To prevent the multi-gigabyte index from being wiped or rebuilt on container restart, the `.index` files must be mapped to a persistent Docker Volume on the host.
3. **Asymmetric Hardware Allocation:** By isolating the service, Kubernetes or Docker Swarm can allocate memory-optimized nodes (high RAM, lower CPU) strictly for the Vector Store, while deploying the Core Engine on standard compute nodes.


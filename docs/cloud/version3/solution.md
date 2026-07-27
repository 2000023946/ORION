
---

# Load Test Analysis: Memory Constraints and Microservice Overhead

![In-Memory Vector DB Core Statistics](microservice_core_stats.png)

![Vector DB Microservice Core Statistics](vector_db_service.png)

## Objective

This study evaluates system stability, latency, and resource utilization between an in-memory monolithic architecture and a microservice architecture under heavy user load within a 4GB RAM environment.

## Executive Summary

The evaluation demonstrates the impact of architectural overhead under strict memory limitations. Although microservice architectures provide scalability and isolation benefits in cloud environments, additional runtime, container, and communication overhead can reduce system resilience on constrained hardware.

## Performance Comparison

| Metric        | In-Memory Monolith         | Microservice Architecture         |
| ------------- | -------------------------- | --------------------------------- |
| Architecture  | Shared 4GB memory pool     | Independent service allocation    |
| Peak Latency  | ~50,000 ms                 | ~0 ms (affected by failure state) |
| Throughput    | Limited by request queuing | High error response rate          |
| Failure Count | ~1,700 request timeouts    | 60,000+ failed requests           |
| System State  | Degraded but operational   | OOMKilled                         |

## Findings

### In-Memory Architecture

The monolithic architecture shared available memory across system components, allowing resources to be allocated dynamically. Under heavy load, the system maintained operation by increasing request queue depth, resulting in high latency but continued processing.

### Microservice Architecture

The microservice deployment introduced additional memory consumption from container isolation, independent runtimes, and service communication overhead. The dedicated vector database service reduced available resources for other components, causing memory exhaustion and service termination.

The observed near-zero latency and increased throughput during failure conditions were not representative of successful processing. Instead, they resulted from rapid request rejection after services were terminated by the operating system.

## Conclusion

Under a 4GB RAM constraint, the monolithic architecture demonstrated higher resilience due to reduced infrastructure overhead and shared resource utilization. Microservice architectures remain effective for scalable cloud deployments; however, their additional operational costs must be considered when deployed on resource-limited systems.

---



# Source Code Architecture

Orion is a **modular, interface-driven Model Context Protocol (MCP) orchestration system** that follows a **Domain-Driven Design (DDD)-inspired layered architecture**. The system emphasizes separation of concerns, dependency inversion, and extensibility through registry-based component resolution.

The architecture is designed to support:

* Separation of business logic from infrastructure
* Pluggable implementations through interfaces
* Dynamic tool discovery using registries
* Deterministic orchestration and testability

---

# System Execution Flow

At runtime, the application follows the execution pipeline shown below:

```text
main.py
   ↓
components/app.py
   ↓
MCP Client
   ↓
Retrieval Planner
   ↓
Graph Executor
   ↓
Tool Execution
   ↓
LLM Response Generation
```

The composition root initializes the application, constructs all dependencies, and coordinates the interaction between the planner, execution engine, and tool infrastructure.

---

# Architectural Layers

## 1. Domain Layer (`domain/`)

The **domain layer** contains the framework-independent business model and defines the core abstractions used throughout the system.

Representative components include:

* Query
* Context
* Tool definitions
* RetrievalPlan (Directed Acyclic Graph)
* SearchAnswer
* Request and response contracts

This layer contains no infrastructure code, networking logic, or language model integrations, allowing it to remain independent of implementation details.

---

## 2. Application Layer (`application/`)

The **application layer** implements the primary use cases that coordinate domain objects and system behavior.

Primary responsibilities include:

* Executing search workflows
* Coordinating retrieval operations
* Producing structured responses

Key components include:

* `SearchUseCase`
* `SearchResponse`

This layer orchestrates interactions between the domain model and the MCP execution infrastructure while remaining independent of infrastructure-specific implementations.

---

## 3. Composition Layer (`components/`)

The **components layer** serves as the application's composition root, where concrete implementations are instantiated and dependencies are assembled.

Its responsibilities include:

* Constructing the MCP client
* Constructing the MCP server
* Initializing the graph executor
* Configuring dependency injection
* Exposing the FastAPI application

This layer is responsible solely for application configuration and startup, avoiding the implementation of business logic.

---

## 4. Infrastructure Layer (`infrastructure/`)

The **infrastructure layer** provides the concrete implementations required by the application.

### Production Implementations (`real/`)

This package contains production-ready implementations, including:

* LLM-driven MCP planner
* MCP server runtime
* Directed Acyclic Graph (DAG) executor
* HTTP client integrations
* Vector search tools
* Web search tools
* Database retrieval tools
* Metadata retrieval tools

### Testing Implementations (`dummy/`)

The testing package provides mock implementations that replace external dependencies during testing.

These implementations enable:

* Offline execution
* Deterministic testing
* Isolation from external APIs
* LLM-independent unit tests

---

# Registry-Based Architecture

Orion employs a **registry-based architecture** to decouple orchestration logic from concrete tool implementations.

Rather than embedding tool-specific logic throughout the execution pipeline, registries provide dynamic mappings between tool identifiers and their associated implementations.

Conceptually, the registry performs the mapping:

```text
Tool Identifier
        ↓
Concrete Tool Implementation
```

This approach enables runtime resolution of tools without requiring modifications to the orchestration pipeline.

---

# Registry Components

## Tool Registry

Located within:

```text
infrastructure/real/mcp_server/tools/core/
```

Primary registry components include:

* `tool_information_registry.py`
* `tool_request_factory_registry.py`
* `tool_output_registry.py`

Collectively, these registries maintain the metadata, construction logic, and output processing required for each supported tool.

---

## Tool Information Registry

The Tool Information Registry stores metadata describing each available tool, including:

* Tool identifier
* Input schema
* Output schema
* Functional description
* Capability metadata

This information is consumed by the MCP planner during retrieval planning to determine which tools are appropriate for satisfying a query.

---

## Tool Request Factory Registry

The Tool Request Factory Registry associates each tool with a corresponding request builder responsible for constructing validated request objects.

Its responsibilities include:

* Building tool-specific request models
* Validating input parameters
* Isolating tool-specific request construction
* Providing a consistent execution interface

This abstraction allows DAG execution nodes to remain independent of tool implementation details.

---

## Tool Output Registry

The Tool Output Registry standardizes responses returned by heterogeneous tools.

Its responsibilities include:

* Normalizing raw tool outputs
* Converting results into domain objects
* Producing consistent output formats across all tools

This standardization simplifies downstream processing and aggregation.

---

# MCP Execution Model

Orion executes retrieval workflows as a **Directed Acyclic Graph (DAG)** generated dynamically by the MCP planner.

The execution process consists of the following stages:

```text
LLM Planner
      ↓
RetrievalPlan (DAG)
      ↓
Graph Executor
      ↓
Registry-Based Tool Resolution
      ↓
Tool Execution
      ↓
Context Aggregation
      ↓
Final LLM Response
```

Each execution node represents an individual retrieval operation. The graph executor resolves the required implementation through the registry system before executing the corresponding tool.

---

# Architectural Benefits of Registry-Based Design

The registry abstraction provides several architectural advantages.

### Dynamic Tool Resolution

Tool execution is determined at runtime through registry lookups rather than hardcoded conditionals, reducing coupling between orchestration and implementation.

### Extensibility

New tools can be integrated by:

1. Implementing the tool interface.
2. Registering the implementation within the appropriate registries.

No modifications to the orchestration pipeline are required.

### Testability

Registry mappings allow production implementations to be replaced with mock implementations during testing, enabling deterministic execution without external services.

### Separation of Responsibilities

The MCP planner determines **which** tools should be used, while the graph executor determines **how** they are executed. This separation preserves clear architectural boundaries between planning and execution.

---

# Component Construction Workflow

Application initialization proceeds through the following stages:

1. Define the core domain models and interfaces.
2. Register available tools and their associated metadata.
3. Construct infrastructure implementations and inject dependencies through the composition layer.
4. Execute retrieval plans using the graph executor, which resolves all tool implementations dynamically through the registry system.

---

# Testing Architecture

The interface-driven design and registry abstraction support comprehensive testing strategies.

By replacing production components with mock implementations, the system enables:

* Isolated unit testing
* Deterministic DAG execution
* Validation of orchestration logic independent of language models
* Testing without external network dependencies

This separation significantly improves reliability and maintainability throughout the development lifecycle.

---

# Design Summary

Orion implements a **DDD-inspired, layered architecture** centered around **interface-based abstractions** and **registry-driven dependency resolution**. The system executes retrieval workflows as dynamically generated Directed Acyclic Graphs (DAGs), allowing planning, execution, and infrastructure concerns to remain independently extensible.

The registry system serves as the primary architectural abstraction, enabling dynamic tool orchestration while minimizing coupling between components. This design supports extensibility, modularity, reproducibility, and comprehensive testing without requiring modifications to the core orchestration pipeline.

from prometheus_client import Histogram, Gauge # type: ignore

component_duration = Histogram(
    "orion_component_duration_ms",
    "Time spent in each Orion component",
    ["component"]
)

component_memory = Gauge(
    "orion_component_memory_mb",
    "Memory used by each Orion component",
    ["component"]
)

# Added CPU utilization metric
component_cpu = Gauge(
    "orion_component_cpu_seconds",
    "CPU time (user + system) consumed by each Orion component",
    ["component"]
)
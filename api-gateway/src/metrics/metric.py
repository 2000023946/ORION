from dataclasses import dataclass
from datetime import datetime


@dataclass
class ComponentMetric:
    timestamp: datetime
    component: str
    duration_ms: float
    memory_mb: float
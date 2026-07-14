from datetime import datetime

from src.metrics.metric import ComponentMetric


def test_component_metric_creation():

    metric = ComponentMetric(
        timestamp=datetime.now(),
        component="vector_search",
        duration_ms=120.5,
        memory_mb=50.2
    )

    assert metric.component == "vector_search"
    assert metric.duration_ms == 120.5
    assert metric.memory_mb == 50.2
    assert isinstance(metric.timestamp, datetime)
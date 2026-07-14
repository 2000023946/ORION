import time

from src.metrics.decorator import (
    measure,
    collector
)



def test_measure_decorator_records_metric():

    # Clear previous metrics
    collector.metrics.clear()


    @measure("test_component")
    def sample_function():

        time.sleep(0.05)

        return "done"



    result = sample_function()


    assert result == "done"


    metrics = collector.get_metrics()


    assert len(metrics) == 1


    metric = metrics[0]


    assert metric.component == "test_component"

    # Should be at least 50ms
    assert metric.duration_ms >= 50

    assert metric.memory_mb >= 0
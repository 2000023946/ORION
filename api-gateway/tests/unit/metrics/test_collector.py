from datetime import datetime
import csv

from src.metrics.collector import MetricsCollector
from src.metrics.metric import ComponentMetric



def test_add_metric():

    collector = MetricsCollector()


    metric = ComponentMetric(
        timestamp=datetime.now(),
        component="planner",
        duration_ms=20.5,
        memory_mb=10.0
    )


    collector.add_metric(metric)


    metrics = collector.get_metrics()


    assert len(metrics) == 1
    assert metrics[0].component == "planner"



def test_export_csv(tmp_path):

    collector = MetricsCollector()


    metric = ComponentMetric(
        timestamp=datetime.now(),
        component="llm",
        duration_ms=500,
        memory_mb=25
    )


    collector.add_metric(metric)


    file_path = tmp_path / "metrics.csv"


    collector.export_csv(str(file_path))


    assert file_path.exists()


    with open(file_path, "r") as file:

        rows = list(csv.reader(file))


    assert rows[0] == [
        "timestamp",
        "component",
        "duration_ms",
        "memory_mb"
    ]


    assert rows[1][1] == "llm"
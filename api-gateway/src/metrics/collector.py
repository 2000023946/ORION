import csv
from typing import List
from .metric import ComponentMetric


class MetricsCollector:

    def __init__(self):
        self.metrics: List[ComponentMetric] = []


    def add_metric(self, metric: ComponentMetric):
        self.metrics.append(metric)


    def get_metrics(self) -> List[ComponentMetric]:
        return self.metrics


    def export_csv(self, filename: str):

        with open(filename, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "timestamp",
                "component",
                "duration_ms",
                "memory_mb"
            ])


            for metric in self.metrics:
                writer.writerow([
                    metric.timestamp.isoformat(),
                    metric.component,
                    metric.duration_ms,
                    metric.memory_mb
                ])
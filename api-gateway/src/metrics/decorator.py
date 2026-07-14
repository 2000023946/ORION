import time
import tracemalloc
from datetime import datetime
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

from .metric import ComponentMetric
from .collector import MetricsCollector


# Preserve function arguments and return type
P = ParamSpec("P")
R = TypeVar("R")


collector = MetricsCollector()


def measure(component_name: str) -> Callable[
    [Callable[P, R]],
    Callable[P, R]
]:
    """
    Decorator that measures execution time and memory usage.
    """

    def decorator(
        function: Callable[P, R]
    ) -> Callable[P, R]:

        @wraps(function)
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs
        ) -> R:

            tracemalloc.start()

            start_time = time.perf_counter()

            result = function(*args, **kwargs)

            end_time = time.perf_counter()

            _, peak_memory = tracemalloc.get_traced_memory()

            tracemalloc.stop()


            duration_ms = (
                end_time - start_time
            ) * 1000

            memory_mb = (
                peak_memory /
                (1024 * 1024)
            )


            metric = ComponentMetric(
                timestamp=datetime.now(),
                component=component_name,
                duration_ms=round(duration_ms, 2),
                memory_mb=round(memory_mb, 2)
            )


            collector.add_metric(metric)


            return result

        return wrapper

    return decorator
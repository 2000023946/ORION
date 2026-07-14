import time
import tracemalloc
import inspect
from datetime import datetime
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

from src.metrics.collector import MetricsCollector
from src.metrics.metric import ComponentMetric


P = ParamSpec("P")
R = TypeVar("R")

collector = MetricsCollector()


def measure(component_name: str):

    def decorator(
        function: Callable[P, R]
    ):

        if inspect.iscoroutinefunction(function):

            @wraps(function)
            async def async_wrapper(
                *args: P.args,
                **kwargs: P.kwargs
            ):

                tracemalloc.start()

                start = time.perf_counter()

                result = await function(*args, **kwargs)

                end = time.perf_counter()

                _, peak = tracemalloc.get_traced_memory()

                tracemalloc.stop()


                collector.add_metric(
                    ComponentMetric(
                        timestamp=datetime.now(),
                        component=component_name,
                        duration_ms=round(
                            (end-start)*1000,
                            2
                        ),
                        memory_mb=round(
                            peak/(1024*1024),
                            2
                        )
                    )
                )

                return result

            return async_wrapper


        @wraps(function)
        def sync_wrapper(
            *args: P.args,
            **kwargs: P.kwargs
        ):

            tracemalloc.start()

            start = time.perf_counter()

            result = function(*args, **kwargs)

            end = time.perf_counter()

            _, peak = tracemalloc.get_traced_memory()

            tracemalloc.stop()


            collector.add_metric(
                ComponentMetric(
                    timestamp=datetime.now(),
                    component=component_name,
                    duration_ms=round(
                        (end-start)*1000,
                        2
                    ),
                    memory_mb=round(
                        peak/(1024*1024),
                        2
                    )
                )
            )

            return result

        return sync_wrapper

    return decorator
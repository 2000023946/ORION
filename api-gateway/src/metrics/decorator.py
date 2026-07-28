import time
import tracemalloc
import inspect
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

from src.metrics.prometheus_metric import component_duration, component_memory, component_cpu


P = ParamSpec("P")
R = TypeVar("R")


def measure(component_name: str):

    def decorator(function: Callable[P, R]):

        if inspect.iscoroutinefunction(function):

            @wraps(function)
            async def async_wrapper(*args, **kwargs):
                tracemalloc.start()
                
                start_wall = time.perf_counter()
                start_cpu = time.process_time() # Tracks CPU time

                result = await function(*args, **kwargs)

                end_cpu = time.process_time()
                end_wall = time.perf_counter()

                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                duration = (end_wall - start_wall) * 1000
                memory = peak / (1024 * 1024)
                cpu_time = end_cpu - start_cpu # Total CPU seconds consumed

                # SEND TO PROMETHEUS
                component_duration.labels(component=component_name).observe(duration)
                component_memory.labels(component=component_name).set(memory)
                component_cpu.labels(component=component_name).set(cpu_time)

                return result

            return async_wrapper

        @wraps(function)
        def sync_wrapper(*args, **kwargs):
            tracemalloc.start()
            
            start_wall = time.perf_counter()
            start_cpu = time.process_time()

            result = function(*args, **kwargs)

            end_cpu = time.process_time()
            end_wall = time.perf_counter()

            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            duration = (end_wall - start_wall) * 1000
            memory = peak / (1024 * 1024)
            cpu_time = end_cpu - start_cpu

            # SEND TO PROMETHEUS
            component_duration.labels(component=component_name).observe(duration)
            component_memory.labels(component=component_name).set(memory)
            component_cpu.labels(component=component_name).set(cpu_time)

            return result

        return sync_wrapper

    return decorator
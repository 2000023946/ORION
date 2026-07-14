import time
import tracemalloc
import inspect
from datetime import datetime
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

from src.metrics.prometheus_metric import component_duration, component_memory


P = ParamSpec("P")
R = TypeVar("R")



def measure(component_name: str):

    def decorator(function: Callable[P,R]):


        if inspect.iscoroutinefunction(function):

            @wraps(function)
            async def async_wrapper(*args, **kwargs):

                tracemalloc.start()

                start = time.perf_counter()

                result = await function(*args, **kwargs)

                end = time.perf_counter()


                _, peak = tracemalloc.get_traced_memory()

                tracemalloc.stop()


                duration = (end-start)*1000

                memory = peak/(1024*1024)


                # SEND TO PROMETHEUS
                component_duration.labels(
                    component=component_name
                ).observe(duration)


                component_memory.labels(
                    component=component_name
                ).set(memory)


                return result


            return async_wrapper



        @wraps(function)
        def sync_wrapper(*args, **kwargs):

            tracemalloc.start()

            start=time.perf_counter()

            result=function(*args, **kwargs)

            end=time.perf_counter()


            _, peak = tracemalloc.get_traced_memory()

            tracemalloc.stop()


            duration=(end-start)*1000

            memory=peak/(1024*1024)



            component_duration.labels(
                component=component_name
            ).observe(duration)


            component_memory.labels(
                component=component_name
            ).set(memory)


            return result


        return sync_wrapper

    return decorator
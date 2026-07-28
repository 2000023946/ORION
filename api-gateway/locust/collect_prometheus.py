import argparse
import csv
import requests
from datetime import datetime


PROMETHEUS_URL = "http://localhost:9090"


def query_prometheus(query: str):
    """
    Execute PromQL query against Prometheus.
    """

    response = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query",
        params={
            "query": query
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data["data"]["result"]



def get_component_latency(component: str):
    """
    Calculate average component latency.

    average =
    sum(rate(metric_sum))
    /
    sum(rate(metric_count))
    """

    query = f"""
    rate(
        orion_component_duration_ms_sum{{
            component="{component}"
        }}[5m]
    )
    /
    rate(
        orion_component_duration_ms_count{{
            component="{component}"
        }}[5m]
    )
    """

    result = query_prometheus(query)

    if not result:
        return None

    # Prometheus returns seconds for rate calculations
    return round(
        float(result[0]["value"][1]),
        2
    )



def get_component_memory(component: str):

    query = f"""
    orion_component_memory_mb{{
        component="{component}"
    }}
    """

    result = query_prometheus(query)

    if not result:
        return None

    return round(
        float(result[0]["value"][1]),
        2
    )



def get_redis_queue_size():
    """
    Query the Redis task queue size metric from Prometheus.
    """
    query = 'redis_key_size{key="orion_queue"}'
    
    result = query_prometheus(query)

    if not result:
        return 0.0

    return round(
        float(result[0]["value"][1]),
        2
    )



def get_components():

    query = """
    count by(component)
    (
        orion_component_duration_ms_count
    )
    """

    result = query_prometheus(query)

    components = []

    for item in result:
        components.append(
            item["metric"]["component"]
        )

    return components



def export_csv(filename):

    components = get_components()

    rows = []
    current_timestamp = datetime.now().isoformat()
    redis_queue_size = get_redis_queue_size()

    for component in components:

        latency = get_component_latency(component)

        memory = get_component_memory(component)

        rows.append(
            {
                "timestamp": current_timestamp,
                "component": component,
                "avg_latency_ms": latency,
                "memory_mb": memory,
                "redis_queue_size": redis_queue_size
            }
        )


    with open(
        filename,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "timestamp",
                "component",
                "avg_latency_ms",
                "memory_mb",
                "redis_queue_size"
            ]
        )

        writer.writeheader()

        writer.writerows(rows)



    print(
        f"Metrics (including Redis queue size: {redis_queue_size}) exported to {filename}"
    )



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output",
        default="prometheus_metrics.csv"
    )


    args = parser.parse_args()


    export_csv(
        args.output
    )
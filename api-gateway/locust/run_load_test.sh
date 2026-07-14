#!/bin/bash

USERS=$1
SPAWN_RATE=$2
RUNTIME=$3


OUTPUT_DIR="baseline_results/${USERS}_users"


mkdir -p "$OUTPUT_DIR"


echo "Starting Locust Load Test"
echo "Users: $USERS"
echo "Spawn Rate: $SPAWN_RATE"
echo "Runtime: $RUNTIME"


locust \
--host=http://localhost:8000 \
--users "$USERS" \
--spawn-rate "$SPAWN_RATE" \
--run-time "$RUNTIME" \
--headless \
--csv="$OUTPUT_DIR/locust" \
--csv-full-history \
> "$OUTPUT_DIR/locust_output.txt" 2>&1


echo "Locust test complete"

python3 collect_prometheus.py \
--output "$OUTPUT_DIR/prometheus_metrics.csv"

python3 generate_report.py \
"$OUTPUT_DIR/locust_output.txt" \
"$OUTPUT_DIR/prometheus_metrics.csv" \
"$OUTPUT_DIR"


echo "Reports saved in $OUTPUT_DIR"

echo "Opening the html report..."

open "$OUTPUT_DIR/locust_report.html"

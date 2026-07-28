import time
import subprocess
import threading
import random
import string
import urllib.request
import urllib.parse
import json
import webbrowser
import os

# ==========================================
# CONFIGURATION
# ==========================================
API_ENDPOINT = "http://localhost:8000/search"
PROMETHEUS_URL = "http://localhost:9090"  # Ensure kubectl port-forward is running!

# Define your test phases: list of tuples (RPS, duration_in_seconds)
TEST_PLAN = [
    (8, 90),
    (16, 90),
    (32, 90),
]

COOLDOWN_SECONDS = 15  # Time to wait between tests to let queues drain

# ==========================================
# INFRASTRUCTURE DISCOVERY
# ==========================================
def get_redis_pod_name():
    try:
        result = subprocess.run(
            ["kubectl", "get", "pods", "-l", "app=orion-redis", "-o", "jsonpath={.items[0].metadata.name}"],
            capture_output=True, text=True, check=True
        )
        pod_name = result.stdout.strip()
        if pod_name: return pod_name
    except Exception as e:
        print(f"[!] Warning: Could not automatically resolve Redis pod name: {e}")
    return "orion-redis"

K8S_REDIS_POD = get_redis_pod_name()
print(f"[*] Target Redis Pod resolved as: {K8S_REDIS_POD}\n")

# ==========================================
# SHARED STATE & WORKERS
# ==========================================
metrics_lock = threading.Lock()
request_logs = []
queue_logs = []
prometheus_logs = []
active_request_threads = []  # Tracks in-flight requests
test_active = False
current_rps = 1

def generate_random_query(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def fire_single_request(start_time_test):
    """Executes a single HTTP request so the main loop isn't blocked."""
    query_text = generate_random_query(10)
    payload = json.dumps({"query": query_text})
    req = urllib.request.Request(
        API_ENDPOINT, data=payload.encode('utf-8'),
        headers={'Content-Type': 'application/json'}, method='POST'
    )
    
    start_time = time.time()
    elapsed = round(start_time - start_time_test, 2)
    start_str = time.strftime('%H:%M:%S', time.localtime(start_time)) + f".{int((start_time % 1) * 1000):03d}"
    
    status_recorded = "UNKNOWN"
    duration_ms = 0.0
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            duration_ms = (time.time() - start_time) * 1000
            status_code = response.getcode()
            status_recorded = "SUCCESS"
            print(f"[REQ: {start_str}] (Duration: {duration_ms:.2f}ms) [SUCCESS] Status: {status_code}")
    except urllib.error.HTTPError as e:
        duration_ms = (time.time() - start_time) * 1000
        status_recorded = f"FAIL_HTTP_{e.code}"
        print(f"[REQ: {start_str}] (Duration: {duration_ms:.2f}ms) [FAIL] HTTP Error: {e.code}")
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        status_recorded = "FAIL_EXCEPTION"
        print(f"[REQ: {start_str}] (Duration: {duration_ms:.2f}ms) [FAIL] Error: {e}")
        
    with metrics_lock:
        request_logs.append({
            "elapsed_sec": elapsed,
            "duration_ms": round(duration_ms, 2),
            "status": status_recorded
        })

def traffic_generator(duration):
    """Maintains a strict RPS rate by spawning threads for each request."""
    global test_active, current_rps, active_request_threads
    start_time_test = time.time()
    
    while test_active and (time.time() - start_time_test < duration):
        t = threading.Thread(target=fire_single_request, args=(start_time_test,), daemon=True)
        t.start()
        
        with metrics_lock:
            active_request_threads.append(t)
            
        time.sleep(1 / current_rps)

def monitor_queue_payloads(duration):
    global test_active
    start_time_test = time.time()
    try:
        while test_active and (time.time() - start_time_test < duration):
            len_result = subprocess.run(
                ["kubectl", "exec", K8S_REDIS_POD, "--", "redis-cli", "llen", "queue:search_tasks"],
                capture_output=True, text=True
            )
            q_str = len_result.stdout.strip()
            q_val = int(q_str) if q_str.isdigit() else 0
            
            with metrics_lock:
                queue_logs.append({
                    "elapsed_sec": round(time.time() - start_time_test, 2),
                    "queue_len": q_val
                })
            time.sleep(1)
    except KeyboardInterrupt:
        pass

def monitor_prometheus_metrics(duration):
    """Queries Prometheus HTTP API to track internal CPU and Memory Gauges."""
    global test_active
    start_time_test = time.time()
    
    cpu_query = urllib.parse.quote('sum(rate(process_cpu_seconds_total{job="orion-executor"}[30s]))')
    mem_query = urllib.parse.quote('sum(process_resident_memory_bytes{job="orion-executor"}) / 1024 / 1024')
    
    try:
        while test_active and (time.time() - start_time_test < duration):
            elapsed = round(time.time() - start_time_test, 2)
            current_cpu = 0.0
            current_mem = 0.0
            
            # Fetch CPU Metric
            try:
                url = f"{PROMETHEUS_URL}/api/v1/query?query={cpu_query}"
                with urllib.request.urlopen(url, timeout=2) as response:
                    data = json.loads(response.read().decode())
                    if data.get('data', {}).get('result'):
                        current_cpu = float(data['data']['result'][0]['value'][1])
            except Exception as e:
                pass # Fail silently so the load test doesn't crash if Prometheus is slow

            # Fetch Memory Metric
            try:
                url = f"{PROMETHEUS_URL}/api/v1/query?query={mem_query}"
                with urllib.request.urlopen(url, timeout=2) as response:
                    data = json.loads(response.read().decode())
                    if data.get('data', {}).get('result'):
                        current_mem = float(data['data']['result'][0]['value'][1])
            except Exception as e:
                pass

            with metrics_lock:
                prometheus_logs.append({
                    "elapsed_sec": elapsed,
                    "cpu": current_cpu,
                    "mem": current_mem
                })
            
            # Sleep 2 seconds (Prometheus scrapes every 5s, so polling every 2s guarantees we catch updates)
            time.sleep(2)
    except KeyboardInterrupt:
        pass

# ==========================================
# MAIN RUNNER & HTML GENERATOR
# ==========================================
def run_test_suite():
    global request_logs, queue_logs, prometheus_logs, test_active, current_rps, active_request_threads
    all_results = {}
    
    total_phases = len(TEST_PLAN)

    for index, (phase_rps, phase_duration) in enumerate(TEST_PLAN):
        print(f"\n{'='*60}\n🚀 STARTING TEST: {phase_rps} RPS for {phase_duration} seconds\n{'='*60}")
        
        # Reset state for new run
        with metrics_lock:
            request_logs = []
            queue_logs = []
            prometheus_logs = []
            active_request_threads = []
            current_rps = phase_rps
            test_active = True
            
        load_thread = threading.Thread(target=traffic_generator, args=(phase_duration,), daemon=True)
        prom_thread = threading.Thread(target=monitor_prometheus_metrics, args=(phase_duration,), daemon=True)
        
        load_thread.start()
        prom_thread.start()
        
        # Run monitor on the main thread for the duration
        monitor_queue_payloads(phase_duration)
        
        # Stop new requests from firing
        test_active = False
        load_thread.join(timeout=2.0)
        prom_thread.join(timeout=2.0)
        
        print("\n[*] Waiting up to 10s for in-flight requests to finish...")
        for t in active_request_threads:
            t.join(timeout=10.0)
        
        # Calculate Phase Statistics
        with metrics_lock:
            total_reqs = len(request_logs)
            success_reqs = sum(1 for r in request_logs if r["status"] == "SUCCESS")
            success_rate = (success_reqs / total_reqs * 100) if total_reqs else 0.0
            
            durations = [r["duration_ms"] for r in request_logs if r["status"] == "SUCCESS"]
            avg_lat = sum(durations)/len(durations) if durations else 0.0
            max_lat = max(durations) if durations else 0.0
            
            q_vals = [q["queue_len"] for q in queue_logs]
            max_q = max(q_vals) if q_vals else 0

            cpu_vals = [p["cpu"] for p in prometheus_logs]
            mem_vals = [p["mem"] for p in prometheus_logs]
            peak_cpu = max(cpu_vals) if cpu_vals else 0.0
            peak_mem = max(mem_vals) if mem_vals else 0.0
            
            run_key = f"{phase_rps} RPS"
            all_results[run_key] = {
                "rps": phase_rps,
                "duration": phase_duration,
                "total_reqs": total_reqs,
                "success_rate": success_rate,
                "avg_lat": avg_lat,
                "max_q": max_q,
                "peak_cpu": peak_cpu,
                "peak_mem": peak_mem,
                "req_labels": [r["elapsed_sec"] for r in request_logs],
                "req_data": [r["duration_ms"] for r in request_logs],
                "q_labels": [q["elapsed_sec"] for q in queue_logs],
                "q_data": [q["queue_len"] for q in queue_logs],
                "prom_labels": [p["elapsed_sec"] for p in prometheus_logs],
                "cpu_data": [p["cpu"] for p in prometheus_logs],
                "mem_data": [p["mem"] for p in prometheus_logs]
            }

        generate_html(all_results)

        if index < total_phases - 1:
            print(f"\n✅ Finished {phase_rps} RPS run. Cooling down for {COOLDOWN_SECONDS}s to let queues drain...\n")
            time.sleep(COOLDOWN_SECONDS)
        else:
            print(f"\n✅ Finished {phase_rps} RPS run. All test phases complete!\n")


def generate_html(results):
    html_filename = "load_test_suite_report.html"
    print(f"[*] Updating HTML report and opening: {html_filename}...")

    labels = list(results.keys())
    avg_lats = [res["avg_lat"] for res in results.values()]
    max_qs = [res["max_q"] for res in results.values()]
    peak_cpus = [res["peak_cpu"] for res in results.values()]
    peak_mems = [res["peak_mem"] for res in results.values()]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>K8s Baseline Suite Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1, h2 {{ color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 10px; }}
        .summary-card {{ background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 40px; }}
        .run-section {{ background: #1e293b; padding: 20px; border-radius: 12px; margin-bottom: 40px; border: 1px solid #334155; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .stat-box {{ background: #0f172a; padding: 15px; border-radius: 8px; border: 1px solid #334155; }}
        .stat-box h4 {{ margin: 0 0 5px 0; font-size: 12px; color: #94a3b8; text-transform: uppercase; }}
        .stat-box .val {{ font-size: 20px; font-weight: bold; color: #f1f5f9; }}
        .chart-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }}
        canvas {{ background: #0f172a; border-radius: 8px; padding: 10px; border: 1px solid #334155; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Kubernetes Microservice Load Test Suite</h1>
        
        <div class="summary-card">
            <h2>Master Summary Comparison</h2>
            
            <!-- First Chart: Performance -->
            <div style="margin-bottom: 40px;">
                <h3 style="text-align: center; color: #94a3b8; font-size: 14px; margin-top: 0;">Performance (Latency vs Queue)</h3>
                <canvas id="summaryChart" style="max-height: 350px;"></canvas>
            </div>
            
            <!-- Second Chart: Resources -->
            <div>
                <h3 style="text-align: center; color: #94a3b8; font-size: 14px; margin-top: 0;">Resources (Peak CPU vs Memory)</h3>
                <canvas id="resourceSummaryChart" style="max-height: 350px;"></canvas>
            </div>
        </div>
"""

    js_scripts = f"""
    <script>
        new Chart(document.getElementById('summaryChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: {labels},
                datasets: [
                    {{ label: 'Avg Latency (ms)', data: {avg_lats}, backgroundColor: '#38bdf8', yAxisID: 'y' }},
                    {{ label: 'Max Queue Depth', data: {max_qs}, backgroundColor: '#a855f7', yAxisID: 'y1' }}
                ]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{ type: 'linear', display: true, position: 'left', title: {{ display: true, text: 'Latency (ms)' }} }},
                    y1: {{ type: 'linear', display: true, position: 'right', title: {{ display: true, text: 'Queue Depth' }}, grid: {{ drawOnChartArea: false }} }}
                }}
            }}
        }});

        new Chart(document.getElementById('resourceSummaryChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: {labels},
                datasets: [
                    {{ label: 'Peak CPU (Cores)', data: {peak_cpus}, backgroundColor: '#facc15', yAxisID: 'y' }},
                    {{ label: 'Peak Memory (MB)', data: {peak_mems}, backgroundColor: '#f87171', yAxisID: 'y1' }}
                ]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{ type: 'linear', display: true, position: 'left', title: {{ display: true, text: 'CPU (Cores)' }} }},
                    y1: {{ type: 'linear', display: true, position: 'right', title: {{ display: true, text: 'Memory (MB)' }}, grid: {{ drawOnChartArea: false }} }}
                }}
            }}
        }});
    """

    for i, (name, data) in enumerate(results.items()):
        html += f"""
        <div class="run-section">
            <h2>{name} Run ({data["duration"]}s)</h2>
            <div class="metrics-grid">
                <div class="stat-box"><h4>Total Requests</h4><div class="val">{data["total_reqs"]}</div></div>
                <div class="stat-box"><h4>Success Rate</h4><div class="val" style="color: #4ade80;">{data["success_rate"]:.1f}%</div></div>
                <div class="stat-box"><h4>Avg Latency</h4><div class="val" style="color: #38bdf8;">{data["avg_lat"]:.1f} ms</div></div>
                <div class="stat-box"><h4>Max Queue</h4><div class="val" style="color: #a855f7;">{data["max_q"]}</div></div>
                <div class="stat-box"><h4>Peak Pod CPU (Cores)</h4><div class="val" style="color: #facc15;">{data["peak_cpu"]:.3f} vCPU</div></div>
                <div class="stat-box"><h4>Peak Pod Memory</h4><div class="val" style="color: #f87171;">{data["peak_mem"]:.1f} MB</div></div>
            </div>
            
            <div class="chart-row">
                <div><canvas id="lat_{i}"></canvas></div>
                <div><canvas id="q_{i}"></canvas></div>
            </div>
            
            <div class="chart-row">
                <div><canvas id="cpu_{i}"></canvas></div>
                <div><canvas id="mem_{i}"></canvas></div>
            </div>
        </div>
        """

        js_scripts += f"""
        new Chart(document.getElementById('lat_{i}').getContext('2d'), {{
            type: 'line',
            data: {{ labels: {data["req_labels"]}, datasets: [{{ label: 'Client Latency (ms)', data: {data["req_data"]}, borderColor: '#38bdf8', borderWidth: 1, pointRadius: 1 }}] }},
            options: {{ responsive: true, plugins: {{ title: {{ display: true, text: 'Client Request Latency', color: '#94a3b8' }}, legend: {{ display: false }} }}, scales: {{ x: {{ title: {{ display: true, text: 'Seconds', color: '#94a3b8' }} }} }} }}
        }});
        new Chart(document.getElementById('q_{i}').getContext('2d'), {{
            type: 'line',
            data: {{ labels: {data["q_labels"]}, datasets: [{{ label: 'Queue Depth', data: {data["q_data"]}, borderColor: '#a855f7', borderWidth: 2, pointRadius: 0, stepped: true }}] }},
            options: {{ responsive: true, plugins: {{ title: {{ display: true, text: 'Redis Task Queue Depth', color: '#94a3b8' }}, legend: {{ display: false }} }}, scales: {{ x: {{ title: {{ display: true, text: 'Seconds', color: '#94a3b8' }} }} }} }}
        }});
        new Chart(document.getElementById('cpu_{i}').getContext('2d'), {{
            type: 'line',
            data: {{ labels: {data["prom_labels"]}, datasets: [{{ label: 'Total vCPU Usage', data: {data["cpu_data"]}, borderColor: '#facc15', borderWidth: 2, pointRadius: 2, stepped: true }}] }},
            options: {{ responsive: true, plugins: {{ title: {{ display: true, text: 'Worker Pod CPU Usage (Cores)', color: '#94a3b8' }}, legend: {{ display: false }} }}, scales: {{ x: {{ title: {{ display: true, text: 'Seconds', color: '#94a3b8' }} }} }} }}
        }});
        new Chart(document.getElementById('mem_{i}').getContext('2d'), {{
            type: 'line',
            data: {{ labels: {data["prom_labels"]}, datasets: [{{ label: 'Total Memory (MB)', data: {data["mem_data"]}, borderColor: '#f87171', borderWidth: 2, pointRadius: 2, stepped: true }}] }},
            options: {{ responsive: true, plugins: {{ title: {{ display: true, text: 'Worker Pod Memory Usage (MB)', color: '#94a3b8' }}, legend: {{ display: false }} }}, scales: {{ x: {{ title: {{ display: true, text: 'Seconds', color: '#94a3b8' }} }} }} }}
        }});
        """

    html += "</div>" + js_scripts + "</script></body></html>"

    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open(f"file://{os.path.abspath(html_filename)}")

if __name__ == "__main__":
    run_test_suite()
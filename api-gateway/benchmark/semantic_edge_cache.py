import asyncio
import json
import os
import time
import webbrowser
import httpx

# Endpoint settings
API_URL = "http://localhost:8000/search"

# 20 Queries organized in 5 semantic intent clusters.
# Query 1 in each cluster will MISS; Queries 2-4 will semantically HIT.
QUERIES = [
    # Cluster 1: KEDA Scaling
    "How do I scale KEDA pods?",
    "What is the process for scaling KEDA worker pods?",
    "Tell me how to scale workers in KEDA",
    "How to increase KEDA pod count",

    # Cluster 2: Redis Queue Metrics
    "How to check Redis queue depth in Grafana?",
    "Where can I see Redis queue depth on Grafana dashboard?",
    "Checking the size of Redis search task queue in Grafana",
    "Show me Redis queue depth metric",

    # Cluster 3: Vector Search & Qdrant
    "How does vector similarity search work in Qdrant?",
    "Explain Qdrant vector similarity matching",
    "How does Qdrant calculate similarity between vectors?",
    "What is vector search in Qdrant?",

    # Cluster 4: Prometheus & FastAPI
    "How to monitor FastAPI latency using Prometheus metrics?",
    "Tracking FastAPI response times with Prometheus",
    "Measuring FastAPI endpoint duration in Prometheus",
    "Prometheus metrics for FastAPI response time",

    # Cluster 5: TEI Embeddings
    "What embedding model size does TEI support?",
    "Which model dimensions work with Text Embeddings Inference?",
    "Supported vector embedding models in TEI",
    "TEI embedding dimension specs"
]

async def run_benchmark():
    results = []
    print(f"🚀 Starting Semantic Cache Benchmark against {API_URL} ({len(QUERIES)} queries)...\n")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        for idx, query_text in enumerate(QUERIES, 1):
            start_time = time.perf_counter()
            is_cached = False
            success = True
            
            try:
                response = await client.post(API_URL, json={"query": query_text})
                elapsed_ms = (time.perf_counter() - start_time) * 1000
                
                if response.status_code == 200:
                    payload = response.json()
                    metadata = payload.get("metadata") or {}
                    is_cached = metadata.get("gateway_cached", False)
                    success = payload.get("success", True)
                else:
                    success = False
            except Exception as err:
                elapsed_ms = (time.perf_counter() - start_time) * 1000
                success = False
                print(f"⚠️ Query {idx} error: {err}")

            tag = "⚡ HIT" if is_cached else "🐢 MISS"
            print(f"[{idx:02d}/{len(QUERIES)}] {elapsed_ms:7.2f} ms | {tag} | \"{query_text}\"")
            
            results.append({
                "id": idx,
                "query": query_text,
                "duration_ms": round(elapsed_ms, 2),
                "cached": is_cached,
                "success": success
            })
            
            # Short pause between queries to observe sequential execution
            await asyncio.sleep(0.15)
            
    return results

def generate_html_report(results):
    hits = [r for r in results if r["cached"]]
    misses = [r for r in results if not r["cached"]]
    
    avg_hit_ms = round(sum(r["duration_ms"] for r in hits) / len(hits), 2) if hits else 0
    avg_miss_ms = round(sum(r["duration_ms"] for r in misses) / len(misses), 2) if misses else 0
    speedup = round(avg_miss_ms / avg_hit_ms, 1) if avg_hit_ms > 0 else 0

    labels_json = json.dumps([f"Q{r['id']}" for r in results])
    data_json = json.dumps([r["duration_ms"] for r in results])
    colors_json = json.dumps(["#10b981" if r["cached"] else "#f59e0b" for r in results])
    
    table_rows = ""
    for r in results:
        badge_class = "badge-hit" if r["cached"] else "badge-miss"
        badge_text = "CACHE HIT" if r["cached"] else "CACHE MISS"
        table_rows += f"""
        <tr>
            <td><strong>#{r['id']}</strong></td>
            <td>{r['query']}</td>
            <td><span class="{badge_class}">{badge_text}</span></td>
            <td style="font-family: monospace;">{r['duration_ms']} ms</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Semantic Edge Cache Benchmark</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
            margin: 0;
            padding: 30px;
        }}
        .container {{
            max-width: 1100px;
            margin: 0 auto;
        }}
        h1 {{
            font-size: 2rem;
            margin-bottom: 5px;
            color: #38bdf8;
        }}
        p.subtitle {{
            color: #94a3b8;
            margin-top: 0;
            margin-bottom: 25px;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 25px;
        }}
        .card {{
            background: #1e293b;
            border-radius: 8px;
            padding: 20px;
            border: 1px solid #334155;
        }}
        .card-title {{
            font-size: 0.85rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .card-value {{
            font-size: 1.8rem;
            font-weight: bold;
            margin-top: 8px;
            color: #f8fafc;
        }}
        .chart-card {{
            background: #1e293b;
            border-radius: 8px;
            padding: 20px;
            border: 1px solid #334155;
            margin-bottom: 25px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: #1e293b;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #334155;
        }}
        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid #334155;
        }}
        th {{
            background-color: #0f172a;
            color: #94a3b8;
            font-weight: 600;
        }}
        .badge-hit {{
            background-color: #064e3b;
            color: #34d399;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .badge-miss {{
            background-color: #78350f;
            color: #fbbf24;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Semantic Edge Cache Performance</h1>
        <p class="subtitle">Orion API Gateway Benchmark Verification</p>

        <div class="metrics-grid">
            <div class="card">
                <div class="card-title">Total Queries</div>
                <div class="card-value">{len(results)}</div>
            </div>
            <div class="card">
                <div class="card-title">Avg Miss Latency</div>
                <div class="card-value" style="color: #fbbf24;">{avg_miss_ms} ms</div>
            </div>
            <div class="card">
                <div class="card-title">Avg Hit Latency</div>
                <div class="card-value" style="color: #34d399;">{avg_hit_ms} ms</div>
            </div>
            <div class="card">
                <div class="card-title">Latency Speedup</div>
                <div class="card-value" style="color: #38bdf8;">{speedup}x Faster</div>
            </div>
        </div>

        <div class="chart-card">
            <canvas id="latencyChart" height="100"></canvas>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Query</th>
                    <th>Query Text</th>
                    <th>Status</th>
                    <th>Latency</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>

    <script>
        const ctx = document.getElementById('latencyChart').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {labels_json},
                datasets: [{{
                    label: 'Response Time (ms)',
                    data: {data_json},
                    backgroundColor: {colors_json},
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }},
                    title: {{
                        display: true,
                        text: 'Query Response Time Sequence (Orange = Cache Miss, Green = Semantic Hit)',
                        color: '#94a3b8'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{ color: '#334155' }},
                        ticks: {{ color: '#94a3b8' }}
                    }},
                    x: {{
                        grid: {{ display: false }},
                        ticks: {{ color: '#94a3b8' }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

    file_path = os.path.abspath("semantic_cache_report.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"\n📊 Benchmark completed successfully!")
    print(f"📄 Report generated: {file_path}")
    webbrowser.open(f"file://{file_path}")

if __name__ == "__main__":
    benchmark_data = asyncio.run(run_benchmark())
    generate_html_report(benchmark_data)
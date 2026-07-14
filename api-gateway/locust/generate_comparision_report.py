import os
import glob
import subprocess
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    # 1. Point the script to look inside the baseline_results directory
    target_directory = "baseline_results"
    
    # Find all directories ending with _users inside baseline_results/
    search_pattern = os.path.join(target_directory, "*_users")
    directories = glob.glob(search_pattern)
    
    if not directories:
        print(f"No *_users directories found in {target_directory}/")
        return

    locust_stats = []
    prom_data = []

    for d in directories:
        try:
            # Extract just the folder name (e.g., '100_users' from 'baseline_results/100_users')
            folder_name = os.path.basename(d)
            users = int(folder_name.split('_')[0])
        except ValueError:
            continue
        
        # Parse Locust Stats (Aggregated Row)
        stats_file = os.path.join(d, "locust_stats.csv")
        if os.path.exists(stats_file):
            try:
                df_stats = pd.read_csv(stats_file)
                agg_row = df_stats[df_stats['Name'] == 'Aggregated']
                if not agg_row.empty:
                    locust_stats.append({
                        'Users': users,
                        'Average Response Time': agg_row.iloc[0]['Average Response Time'],
                        'Requests/s': agg_row.iloc[0]['Requests/s'],
                        'Failures': agg_row.iloc[0]['Failure Count']
                    })
            except Exception as e:
                print(f"Error reading {stats_file}: {e}")

        # Parse Prometheus Metrics
        prom_file = os.path.join(d, "prometheus_metrics.csv")
        if os.path.exists(prom_file):
            try:
                df_prom = pd.read_csv(prom_file)
                if not df_prom.empty:
                    prom_agg = df_prom.groupby('component')[['avg_latency_ms', 'memory_mb']].mean().reset_index()
                    for _, row in prom_agg.iterrows():
                        prom_data.append({
                            'Users': users,
                            'Component': row['component'],
                            'Avg Latency (ms)': row['avg_latency_ms'],
                            'Memory (MB)': row['memory_mb']
                        })
            except Exception as e:
                print(f"Error reading {prom_file}: {e}")

    # Create DataFrames and sort by number of users
    df_stats_plot = pd.DataFrame(locust_stats).sort_values(by='Users') if locust_stats else pd.DataFrame()
    df_prom_plot = pd.DataFrame(prom_data).sort_values(by='Users') if prom_data else pd.DataFrame()

    if df_stats_plot.empty and df_prom_plot.empty:
        print("No data found to plot.")
        return

    # Start building the HTML file
    html_content = """
    <html>
    <head>
        <title>Comprehensive Load Test Dashboard</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 20px; background-color: #f8f9fa; }
            .container { max-width: 1400px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h1 { text-align: center; color: #333; }
            .chart-container { margin-bottom: 40px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Comprehensive Load Test & Metrics Dashboard</h1>
    """

    # Figure 1: Locust Load Test Stats
    if not df_stats_plot.empty:
        fig1 = make_subplots(rows=1, cols=3, subplot_titles=("Average Response Time (ms)", "Throughput (Requests/s)", "Failures"))
        
        fig1.add_trace(go.Scatter(x=df_stats_plot['Users'], y=df_stats_plot['Average Response Time'], mode='lines+markers', name='Response Time', line=dict(color='#3498db', width=3)), row=1, col=1)
        fig1.add_trace(go.Scatter(x=df_stats_plot['Users'], y=df_stats_plot['Requests/s'], mode='lines+markers', name='Requests/s', line=dict(color='#2ecc71', width=3)), row=1, col=2)
        fig1.add_trace(go.Scatter(x=df_stats_plot['Users'], y=df_stats_plot['Failures'], mode='lines+markers', name='Failures', line=dict(color='#e74c3c', width=3)), row=1, col=3)
        
        fig1.update_layout(height=450, showlegend=False, template="plotly_white", margin=dict(t=40, b=40, l=40, r=40))
        fig1.update_xaxes(title_text="Number of Users")
        
        html_content += f"<div class='chart-container'><h2>Locust Core Statistics</h2>{fig1.to_html(full_html=False, include_plotlyjs='cdn')}</div>"

    # Figures 2 & 3: Prometheus Metrics (Latency & Memory)
    if not df_prom_plot.empty:
        components = df_prom_plot['Component'].unique()
        
        # Prometheus Latency
        fig2 = go.Figure()
        for comp in components:
            df_c = df_prom_plot[df_prom_plot['Component'] == comp]
            fig2.add_trace(go.Scatter(x=df_c['Users'], y=df_c['Avg Latency (ms)'], mode='lines+markers', name=comp, line=dict(width=2.5)))
        
        fig2.update_layout(title="Component Latency vs Users", xaxis_title="Number of Users", yaxis_title="Average Latency (ms)", height=500, template="plotly_white", hovermode="x unified")
        html_content += f"<div class='chart-container'><h2>Prometheus: Component Latency</h2>{fig2.to_html(full_html=False, include_plotlyjs=False)}</div>"

        # Prometheus Memory
        fig3 = go.Figure()
        for comp in components:
            df_c = df_prom_plot[df_prom_plot['Component'] == comp]
            fig3.add_trace(go.Scatter(x=df_c['Users'], y=df_c['Memory (MB)'], mode='lines+markers', name=comp, line=dict(width=2.5)))
            
        fig3.update_layout(title="Component Memory vs Users", xaxis_title="Number of Users", yaxis_title="Memory (MB)", height=500, template="plotly_white", hovermode="x unified")
        html_content += f"<div class='chart-container'><h2>Prometheus: Component Memory</h2>{fig3.to_html(full_html=False, include_plotlyjs=False)}</div>"

    html_content += """
        </div>
    </body>
    </html>
    """

    # This will save the HTML file in the current directory (the locust directory)
    output_filename = "baseline_results/comprehensive_metrics_dashboard.html"
    with open(output_filename, "w") as f:
        f.write(html_content)
    
    print(f"Success! Created {output_filename} in the current directory.")
    # should open now 
    subprocess.run(["open", output_filename])

if __name__ == '__main__':
    main()
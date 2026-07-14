import re
import sys
import os
import csv
from collections import defaultdict


def parse_locust_log(log_text):
    """
    Parse Locust terminal output.
    """

    users_match = re.search(
        r'Ramping to (\d+) users',
        log_text
    )

    rate_match = re.search(
        r'at a rate of ([\d.]+) per second',
        log_text
    )


    users = (
        users_match.group(1)
        if users_match
        else "Unknown"
    )

    rate = (
        rate_match.group(1)
        if rate_match
        else "Unknown"
    )


    # Final stats section
    parts = log_text.split("Shutting down")

    final_section = parts[-1]


    stats_pattern = (
        r'POST\s+/search\s+'
        r'(\d+)\s+'
        r'(\d+)\(([\d.]+)%\)\s+\|\s+'
        r'(\d+)\s+'
        r'(\d+)\s+'
        r'(\d+)\s+'
        r'(\d+)\s+\|\s+'
        r'([\d.]+)\s+'
        r'([\d.]+)'
    )


    stats_match = re.search(
        stats_pattern,
        final_section
    )


    if stats_match:

        (
            reqs,
            fails,
            fail_pct,
            avg,
            minimum,
            maximum,
            median,
            req_s,
            fail_s
        ) = stats_match.groups()

    else:

        reqs = fails = fail_pct = "N/A"
        avg = minimum = maximum = median = "N/A"
        req_s = fail_s = "N/A"



    percentile_pattern = (
        r'POST\s+/search\s+'
        r'\d+\s+'
        r'\d+\s+'
        r'(\d+)\s+'
        r'(\d+)\s+'
        r'(\d+)\s+'
        r'(\d+)\s+'
        r'(\d+)\s+'
        r'(\d+)\s+'
        r'(\d+)\s+'
        r'(\d+)\s+'
        r'(\d+)\s+'
        r'(\d+)'
    )


    percentile_match = re.search(
        percentile_pattern,
        final_section
    )


    if percentile_match:
        
        values = percentile_match.groups()

        # pad missing percentiles
        values = list(values)

        while len(values) < 11:
            values.insert(-1, "N/A")


        (
            p50,
            p66,
            p75,
            p80,
            p90,
            p95,
            p98,
            p99,
            p999,
            p9999,
            p100
        ) = values

    else:

        (
            p50,
            p66,
            p75,
            p80,
            p90,
            p95,
            p98,
            p99,
            p999,
            p9999,
            p100
        ) = ("N/A",)*11



    return {

        "users": users,

        "rate": rate,

        "stats": {

            "reqs": reqs,
            "fails": fails,
            "fail_pct": fail_pct,
            "avg": avg,
            "min": minimum,
            "max": maximum,
            "median": median,
            "req_s": req_s,
            "fail_s": fail_s

        },


        "percentiles": {

            "p50": p50,
            "p66": p66,
            "p75": p75,
            "p80": p80,
            "p90": p90,
            "p95": p95,
            "p98": p98,
            "p99": p99,
            "p999": p999,
            "p9999": p9999,
            "p100": p100

        }

    }



def parse_prometheus_csv(path):

    """
    Read component latency metrics.
    """


    components = defaultdict(
        lambda:{
            "latency":[],
            "memory":[]
        }
    )


    with open(path) as file:

        reader = csv.DictReader(file)


        for row in reader:


            component = row["component"]


            components[component]["latency"].append(
                float(row["avg_latency_ms"])
            )


            components[component]["memory"].append(
                float(row["memory_mb"])
            )



    results=[]


    for component,data in components.items():

        results.append({

            "component": component,

            "latency":
                sum(data["latency"]) /
                len(data["latency"]),


            "memory":
                sum(data["memory"]) /
                len(data["memory"])

        })



    return sorted(
        results,
        key=lambda x:x["latency"],
        reverse=True
    )



def generate_html(data, components, output_file):


    component_rows=""


    for c in components:

        component_rows += f"""

<tr>

<td>{c['component']}</td>

<td>{c['latency']:.2f}</td>

<td>{c['memory']:.2f}</td>

</tr>

"""


    html=f"""

<!DOCTYPE html>

<html>

<head>

<title>
Locust Load Test Report
</title>


<style>


body {{

font-family:
Arial,
Helvetica,
sans-serif;

background:#f4f6f8;

padding:30px;

color:#333;

}}


.container {{

background:white;

padding:30px;

border-radius:10px;

max-width:1200px;

margin:auto;

}}



h1,h2 {{

color:#2c3e50;

}}



table {{

width:100%;

border-collapse:collapse;

margin-bottom:35px;

}}



th {{

background:#34495e;

color:white;

padding:12px;

}}



td {{

padding:10px;

border-bottom:1px solid #ddd;

text-align:center;

}}



tr:nth-child(even) {{

background:#f9f9f9;

}}



.summary {{

background:#eaf6ff;

padding:15px;

border-left:5px solid #3498db;

}}


</style>


</head>


<body>


<div class="container">


<h1>
Locust Load Test Report
</h1>



<div class="summary">


<h2>
Test Execution Details
</h2>


<p>
<b>Target Load:</b>
{data['users']} users
</p>


<p>
<b>Spawn Rate:</b>
{data['rate']} users/second
</p>


<p>
<b>Status:</b>
Completed
</p>


</div>



<h2>
Request Statistics
</h2>


<table>


<tr>

<th>Type</th>
<th>Name</th>
<th>Requests</th>
<th>Fails</th>
<th>Average(ms)</th>
<th>Min(ms)</th>
<th>Max(ms)</th>
<th>Median(ms)</th>
<th>Req/s</th>
<th>Failures/s</th>

</tr>



<tr>

<td>POST</td>

<td>/search</td>

<td>{data['stats']['reqs']}</td>

<td>{data['stats']['fails']} ({data['stats']['fail_pct']}%)</td>

<td>{data['stats']['avg']}</td>

<td>{data['stats']['min']}</td>

<td>{data['stats']['max']}</td>

<td>{data['stats']['median']}</td>

<td>{data['stats']['req_s']}</td>

<td>{data['stats']['fail_s']}</td>

</tr>


</table>





<h2>
Response Time Percentiles
</h2>


<table>


<tr>

<th>50%</th>
<th>66%</th>
<th>75%</th>
<th>80%</th>
<th>90%</th>
<th>95%</th>
<th>98%</th>
<th>99%</th>
<th>99.9%</th>
<th>99.99%</th>
<th>100%</th>

</tr>


<tr>

<td>{data['percentiles']['p50']} ms</td>

<td>{data['percentiles']['p66']} ms</td>

<td>{data['percentiles']['p75']} ms</td>

<td>{data['percentiles']['p80']} ms</td>

<td>{data['percentiles']['p90']} ms</td>

<td>{data['percentiles']['p95']} ms</td>

<td>{data['percentiles']['p98']} ms</td>

<td>{data['percentiles']['p99']} ms</td>

<td>{data['percentiles']['p999']} ms</td>

<td>{data['percentiles']['p9999']} ms</td>

<td>{data['percentiles']['p100']} ms</td>

</tr>


</table>





<h2>
Component Performance
</h2>


<table>


<tr>

<th>
Component
</th>

<th>
Average Latency(ms)
</th>

<th>
Memory(MB)
</th>


</tr>


{component_rows}


</table>




</div>


</body>


</html>

"""


    with open(output_file,"w") as f:

        f.write(html)



    print(
        f"Report generated: {output_file}"
    )




if __name__=="__main__":


    if len(sys.argv)!=4:

        print(
            "Usage:"
            "python generate_report.py "
            "<locust_output.txt> "
            "<prometheus_metrics.csv> "
            "<output_directory>"
        )

        sys.exit(1)



    locust_file=sys.argv[1]

    prometheus_file=sys.argv[2]

    output_directory=sys.argv[3]



    os.makedirs(
        output_directory,
        exist_ok=True
    )



    with open(locust_file) as f:

        log=f.read()



    locust_data=parse_locust_log(log)


    component_data=parse_prometheus_csv(
        prometheus_file
    )



    output_file=os.path.join(
        output_directory,
        "locust_report.html"
    )



    generate_html(
        locust_data,
        component_data,
        output_file
    )
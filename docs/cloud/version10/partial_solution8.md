## Load Test Incident Report

**Configuration Context:**

* **Target Load:** 16 RPS (90-second duration)
* **Pod Sizing:** 0.5 vCPU
* **Worker Count:** 120 concurrent workers

### Observable Event Summary

During the most recent 16 RPS load test under the **0.5 vCPU / 120 worker** configuration, the system experienced a complete halt in successful processing. Based strictly on the provided log data, here is exactly what occurred:

* **100% Timeout Rate:** Every logged request in the sequence failed with an `Error: timed out` flag.
* **Uniform Failure Threshold:** Every single failure occurred at exactly the ~10,000ms (10-second) mark.
* **Total Processing Gridlock:** The logs demonstrate that requests were ingested by the system sequentially, but zero tasks successfully completed their lifecycle and returned a response before the hard 10-second client-side timeout was triggered.

### Raw Telemetry Snapshot

The system behavior remained strictly uniform throughout the tested window, with no variations or recoveries in the error state. Every logged request hit the exact same 10-second wall:

| Request Timestamp | Duration | Status | Error |
| --- | --- | --- | --- |
| `15:22:43.170` | 10032.94ms | **FAIL** | timed out |
| `15:22:43.237` | 10002.66ms | **FAIL** | timed out |
| `...` | `...` | `...` | `...` |
| `15:22:54.403` | 10002.48ms | **FAIL** | timed out |
| `15:22:54.467` | 10002.05ms | **FAIL** | timed out |

**Conclusion of Run:** Under the 0.5 vCPU and 120 worker parameters, the system successfully received the incoming 16 RPS load but failed to resolve any of those requests within the required 10-second operational window, resulting in a flatline timeout cascade.
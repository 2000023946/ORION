### Configuring Concurrent Users and Ramp-Up Rate in Locust

Locust defines the workload using two independent parameters: the **target number of concurrent users** and the **user spawn rate (ramp-up rate)**.

#### Target Concurrent Users

The **number of users** specifies the maximum number of virtual users that will execute requests concurrently during the test. Once the target is reached, Locust maintains approximately that level of concurrency for the remainder of the test duration.

For example:

```text
Number of users: 100
```

This configuration instructs Locust to maintain approximately **100 concurrent virtual users** throughout the execution of the workload.

#### Ramp-Up Rate

The **spawn rate** (or ramp-up rate) determines the rate at which virtual users are created until the target concurrency is reached.

For example:

```text
Number of users: 100
Spawn rate: 10 users/second
```

The resulting workload progresses as follows:

```text
Time 0 s   →   0 users
Time 1 s   →  10 users
Time 2 s   →  20 users
Time 3 s   →  30 users
...
Time 10 s  → 100 users
```

After the target of 100 concurrent users is reached, Locust continues executing the workload at approximately that concurrency level for the remainder of the test.

### Experimental Workload Configuration

The baseline Orion evaluation may be performed using the following workload configurations:

| Workload Level | Concurrent Users | Spawn Rate |  Duration |
| -------------- | ---------------: | ---------: | --------: |
| Light          |               50 |  5 users/s | 3 minutes |
| Medium         |              100 | 10 users/s | 3 minutes |
| Heavy          |              250 | 25 users/s | 3 minutes |
| Stress         |              500 | 50 users/s | 3 minutes |

In these experiments, the spawn rate serves only to control the transition from an idle system to the desired concurrency level. It is **not** considered an independent experimental variable and is therefore excluded from performance comparisons. Performance metrics should be collected only after the target concurrency has been established.

### Example Methodology Statement

> The monolithic Orion architecture was evaluated under workloads of 50, 100, 250, and 500 concurrent virtual users. Each workload was configured with a spawn rate equal to 10% of the target concurrency per second and executed for a duration of three minutes. The spawn rate was selected solely to achieve a controlled transition to the target workload and was not treated as an experimental variable. This configuration enables reproducible performance evaluation across all workload levels.

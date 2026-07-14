Yes, Locust separates those two:

### 1. Number of users

This is your **maximum concurrent users** (the load level).

Example:

```
Number of users: 100
```

means:

> Locust will eventually have 100 virtual users running at the same time.

---

### 2. Ramp up (spawn rate)

This is **how quickly Locust creates those users**.

Example:

```
Number of users: 100
Ramp up: 10 users/sec
```

means:

```
Time 0s     → 0 users
Time 1s     → 10 users
Time 2s     → 20 users
Time 3s     → 30 users
...
Time 10s    → 100 users
```

After that, it maintains ~100 concurrent users for the duration.

---

For your Orion baseline, I would use:

### Light load

```
Users: 50
Ramp up: 5 users/sec
Duration: 3 minutes
```

### Medium load

```
Users: 100
Ramp up: 10 users/sec
Duration: 3 minutes
```

### Heavy load

```
Users: 250
Ramp up: 25 users/sec
Duration: 3 minutes
```

### Stress load

```
Users: 500
Ramp up: 50 users/sec
Duration: 3 minutes
```

The ramp-up is not part of your performance comparison. It only controls how quickly you reach the target concurrency.

Your report should say something like:

> "The monolithic Orion architecture was evaluated under 50, 100, 250, and 500 concurrent users with a ramp-up rate of 10% of the target concurrency per second."

That makes the experiment reproducible.

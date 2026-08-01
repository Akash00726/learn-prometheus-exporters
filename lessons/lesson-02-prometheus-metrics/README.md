# Lesson 02 - Understanding Prometheus Metric Types

## Objective

In this lesson you will learn:

* Why Prometheus has different metric types
* The difference between Gauge and Counter
* Why Counter only increases
* Why `Counter` does not provide `dec()`
* The difference between `set()` and `inc()`
* When to use Gauge and Counter

> **We will only code Gauge and Counter in this lesson.**
>
> Histogram, Summary and Labels will be covered later after we completely understand these two metric types.

---

# Theory

In Lesson 01, we learned that a Prometheus exporter exposes metrics through the `/metrics` endpoint.

Now let's answer a new question.

**If every metric is just a number, why does Prometheus have multiple metric types?**

The answer lies in **what the number represents**.

Some values represent the **current state**.

Some values represent **history**.

Prometheus uses different metric types to model these different behaviors.

---

## Current State

Examples:

```text
CPU Usage

Memory Usage

Temperature

Disk Usage

Running Pods

Queue Length
```

These values can increase or decrease at any time.

Example:

```text
CPU Usage

20%

45%

72%

31%

18%
```

The latest value is the only thing that matters.

For these metrics we use:

**Gauge**

---

## Historical Totals

Examples:

```text
HTTP Requests

Errors

Files Processed

Failed Logins

Emails Sent
```

Example:

```text
Requests

100

120

145

180

250
```

Once a request has been processed, it cannot become "unprocessed".

These values only increase.

For these metrics we use:

**Counter**

---

# Gauge

A Gauge represents the **current state**.

It can:

* Increase
* Decrease
* Stay the same

Primary operation:

```python
set(value)
```

Examples:

* CPU Usage
* Memory Usage
* Temperature
* Active Sessions
* Running Pods

Think of a Gauge as a speedometer.

The needle moves up and down depending on the current state.

---

# Counter

A Counter represents a **cumulative total**.

It:

* Starts at zero
* Only increases
* Never decreases

Primary operation:

```python
inc()
```

or

```python
inc(value)
```

Examples:

* Requests Served
* Errors
* Jobs Processed
* Login Attempts

Think of a Counter as an odometer.

The reading keeps increasing throughout the lifetime of the process.

---

# Gauge vs Counter

| Gauge               | Counter                 |
| ------------------- | ----------------------- |
| Current State       | Historical Total        |
| `set()`             | `inc()`                 |
| Can increase        | Can increase            |
| Can decrease        | Cannot decrease         |
| Stores latest value | Stores cumulative total |

---

# Hands-on Tasks

## Task 1 - Create a Gauge

Create a metric named:

```text
temperature_celsius
```

Set its value to:

```text
25
```

Verify that it appears in:

```text
http://localhost:8000/metrics
```

### Observe

Locate:

```text
# HELP
# TYPE
temperature_celsius
```

---

## Task 2 - Prediction

Before writing any Counter code, answer:

Suppose we create:

```python
requests = Counter(
    "requests_total",
    "Total Requests"
)
```

and execute:

```python
requests.inc()
requests.inc()
requests.inc()
```

Predict:

1. What value will appear?
2. Where does the value start?
3. Does `inc()` replace the value or add to it?

Only after making your prediction should you run the code.

---

## Task 3 - Build a Counter

Create:

```python
requests = Counter(
    "requests_total",
    "Total Requests"
)
```

Increment it every two seconds.

Example:

```python
while True:

    requests.inc()

    time.sleep(2)
```

Verify:

```text
requests_total
```

Refresh `/metrics` multiple times.

Observe how the value changes.

---

## Task 4 - Can a Counter Decrease?

Before searching documentation, predict:

Does this exist?

```python
requests.dec()
```

Now test it.

Observe the exact error message.

Questions:

1. Does the exporter start?
2. What error occurs?
3. Why do you think the library designers intentionally omitted this method?

---

## Task 5 - Increment by More Than One

Modify:

```python
requests.inc()
```

to

```python
requests.inc(5)
```

Observe the metric.

Questions:

1. Why does `inc()` accept a number?
2. Can you think of situations where adding 5 or 100 at once is more appropriate than incrementing one by one?

Hint:

Think about:

* Batch processing
* Queue processing
* Kubernetes
* Log processing

---

## Task 6 - Compare Gauge and Counter

Create both metrics.

```text
temperature_celsius

requests_total
```

Now update them differently.

Temperature:

```text
20

25

22

30

18
```

Requests:

```text
1

2

3

4

5
```

Observe how they behave.

Questions:

1. Which metric represents the current state?
2. Which metric represents accumulated history?

---

# What You Learned

At this point you should understand:

* Why Gauge exists
* Why Counter exists
* Why Counter uses `inc()`
* Why Gauge uses `set()`
* Why Counter does not have `dec()`
* The difference between current state and cumulative totals

---

# Knowledge Check

Answer these questions in your own words.

1. What problem does Gauge solve?
2. What problem does Counter solve?
3. Why shouldn't CPU usage be a Counter?
4. Why shouldn't HTTP requests be a Gauge?
5. What is the difference between `set()` and `inc()`?
6. Why doesn't Counter provide `dec()`?
7. What happens when `Counter.inc(5)` is called?
8. Give three real-world examples of Gauge.
9. Give three real-world examples of Counter.
10. If you had to monitor "currently running Kubernetes Pods", which metric type would you choose and why?

Do not continue until you can answer these confidently.

---

# Next Lesson

In Lesson 03 we will answer another important question.

**What happens when a Counter resets to zero after an application restart?**

You'll learn:

* Why this is expected behavior
* How Prometheus handles counter resets
* Why counters are still reliable
* Introduction to PromQL functions such as `rate()`

This is one of the most common interview topics related to Prometheus.

# Lesson 02 - Understanding Prometheus Metric Types

## Objective

By the end of this lesson you will understand:

* Why Prometheus has different metric types
* The difference between Gauge and Counter
* When to use each metric type
* Why Counter only supports increment operations
* Why Counters reset after application restart
* How Prometheus recognizes Counter resets
* What Labels are and why they are essential
* How Labels create multiple time series from a single metric

> **In this lesson we focus on Gauge, Counter and Labels.**
>
> Histogram and Summary will be covered in a later lesson.

---

# Theory

In Lesson 01 we learned that an exporter exposes metrics through the `/metrics` endpoint.

Now we need to understand an important question.

> **If every metric is just a number, why does Prometheus have different metric types?**

The answer is simple.

Different numbers represent different kinds of information.

Some represent the **current state**.

Some represent **historical totals**.

Prometheus uses different metric types to represent those different behaviors.

---

# Gauge

A Gauge represents the **current state**.

A Gauge can:

* Increase
* Decrease
* Stay the same

Examples:

* CPU Usage
* Memory Usage
* Temperature
* Queue Length
* Running Pods
* Active Sessions

Primary operation:

```python
set(value)
```

Example:

```python
temperature.set(25)

temperature.set(30)

temperature.set(22)
```

Current value:

```text
22
```

A Gauge always represents the latest state.

---

# Counter

A Counter represents a **cumulative total**.

A Counter:

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

* HTTP Requests
* Errors
* Files Processed
* Login Attempts
* Messages Processed

Example:

```python
requests.inc()

requests.inc()

requests.inc(5)
```

Current value:

```text
7
```

Unlike Gauge, Counter accumulates values.

---

# Why Counter Does Not Have dec()

A Counter represents something that has already happened.

For example:

```text
HTTP Requests

Errors

Emails Sent
```

These events cannot be undone.

If a library allowed:

```python
requests.dec()
```

the metric would lose its meaning.

For this reason, the Prometheus client intentionally does not provide a `dec()` method for Counter.

The API itself prevents incorrect usage.

---

# Gauge vs Counter

| Gauge         | Counter           |
| ------------- | ----------------- |
| Current State | Historical Total  |
| Can increase  | Can increase      |
| Can decrease  | Cannot decrease   |
| Uses `set()`  | Uses `inc()`      |
| Latest value  | Accumulated value |

---

# Counter Reset

During the lifetime of a process, a Counter never decreases.

However, when the application restarts:

```text
Old Process

requests_total = 17

↓

Application Stops

↓

New Process

requests_total = 0
```

The Counter did **not** decrease.

The original Counter no longer exists.

A brand new process creates a brand new Counter.

---

# How Prometheus Handles Counter Reset

Suppose Prometheus observes:

```text
15

16

17

0

1

2
```

Prometheus knows that Counters are not allowed to decrease.

Therefore:

```text
17

↓

0
```

is interpreted as a **Counter Reset**, not a negative value.

Prometheus continues calculating rates correctly by recognizing that a new Counter has started.

This is one of the reasons why selecting the correct metric type is important.

---

# Labels

Without Labels you might create metrics like:

```text
frontend_cpu

backend_cpu

database_cpu
```

As your application grows, the number of metric names grows as well.

Instead, Prometheus encourages using a single metric with labels.

Example:

```text
pod_cpu{pod="frontend"}

pod_cpu{pod="backend"}

pod_cpu{pod="database"}
```

The metric name remains the same.

The labels identify the resource.

---

# Creating a Label

Example:

```python
temperature = Gauge(
    "room_temperature",
    "Room Temperature",
    ["room"]
)
```

Here:

```text
room
```

is the label name.

---

# Setting Label Values

Example:

```python
temperature.labels(room="bedroom").set(25)

temperature.labels(room="kitchen").set(28)

temperature.labels(room="office").set(24)
```

Output:

```text
room_temperature{room="bedroom"} 25

room_temperature{room="kitchen"} 28

room_temperature{room="office"} 24
```

Notice that the metric name never changes.

Only the labels do.

---

# Parent Metric and Time Series

This is an important concept.

When you create:

```python
temperature = Gauge(
    "room_temperature",
    "Room Temperature",
    ["room"]
)
```

you create the **parent metric**.

When you call:

```python
temperature.labels(room="bedroom")
```

the client creates (or retrieves) a specific **time series**.

Conceptually:

```text
room_temperature

├── bedroom

├── kitchen

└── office
```

Each label combination represents an independent time series with its own value.

---

# Hands-on Tasks

## Task 1

Create a Gauge named:

```text
temperature_celsius
```

Set different values using:

```python
set()
```

Observe the metric in:

```text
http://localhost:8000/metrics
```

---

## Task 2

Predict the output of:

```python
requests = Counter(
    "requests_total",
    "Total Requests"
)

requests.inc()

requests.inc()

requests.inc()
```

Run the code and compare the result with your prediction.

---

## Task 3

Create a Counter.

Increment it every two seconds.

Observe that the value only increases.

---

## Task 4

Attempt to execute:

```python
requests.dec()
```

Observe the error.

Explain why the API intentionally does not provide this method.

---

## Task 5

Replace:

```python
requests.inc()
```

with

```python
requests.inc(5)
```

Observe how the Counter behaves.

Think about real-world situations where incrementing by more than one is useful.

---

## Task 6

Run the exporter.

Allow the Counter to reach approximately:

```text
15
```

Stop the exporter.

Restart it.

Observe:

```text
requests_total
```

Explain why the Counter starts from zero again.

---

## Task 7

Create a Gauge with one label.

Example:

```python
temperature = Gauge(
    "room_temperature",
    "Room Temperature",
    ["room"]
)
```

---

## Task 8

Create three label values.

Example:

```python
temperature.labels(room="bedroom").set(25)

temperature.labels(room="kitchen").set(28)

temperature.labels(room="office").set(24)
```

Observe the output in `/metrics`.

---

## Task 9

Explain the difference between:

```python
temperature
```

and

```python
temperature.labels(room="bedroom")
```

Which one represents the parent metric?

Which one represents an individual time series?

---

# Knowledge Check

Answer these questions before moving to the next lesson.

1. Why does Prometheus have multiple metric types?
2. When should you use Gauge?
3. When should you use Counter?
4. Why does Counter not provide `dec()`?
5. What is the difference between `set()` and `inc()`?
6. Why does a Counter reset after an application restart?
7. Did the Counter actually decrease after restart?
8. How does Prometheus recognize a Counter reset?
9. What problem do Labels solve?
10. Why are Labels preferred over creating hundreds of different metric names?
11. What is the difference between a parent metric and a time series?
12. Give three examples where you would use Labels in a Kubernetes exporter.

If you cannot confidently answer these questions, repeat the hands-on tasks before continuing.

---

# Next Lesson

In Lesson 03 we will replace our manually generated values with real system metrics.

You'll learn how to collect:

* CPU Usage
* Memory Usage
* Disk Usage

using Python and expose them as real Prometheus metrics.

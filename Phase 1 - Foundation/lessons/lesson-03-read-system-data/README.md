# Lesson 03 - Read System Data

## Objective

By the end of this lesson you will understand:

* What a data source is
* Why exporters collect data before exposing it
* How to collect real system metrics using Python
* How to expose real system metrics through Prometheus
* The separation between data collection and metric exposure

In this lesson we will collect:

* CPU Usage
* Memory Usage
* Disk Usage

using Python instead of manually assigning values.

---

# Theory

In Lesson 01 we learned how Prometheus metrics are exposed.

In Lesson 02 we learned how different metric types behave.

Until now, every metric value has been manually assigned.

Example:

```python
temperature.set(25)
```

This is useful for learning, but real exporters never invent values.

Instead, they collect information from an external source.

---

# What is a Data Source?

A data source is anything from which an exporter can collect information.

Examples include:

* Operating System
* Kubernetes API Server
* HTTP APIs
* Databases
* Cloud Providers
* Security Platforms
* Log Files

Every exporter follows the same pattern.

```text
Read Data
      │
      ▼
Process Data
      │
      ▼
Update Metric
      │
      ▼
Expose through /metrics
```

The only thing that changes is the data source.

---

# Exporter Architecture

In the previous lessons our exporter looked like this.

```text
Browser / Prometheus
          │
          ▼
     /metrics Endpoint
          │
          ▼
   Collector Registry
          │
          ▼
         Gauge
```

Now we introduce a new component.

```text
Browser / Prometheus
          │
          ▼
     /metrics Endpoint
          │
          ▼
   Collector Registry
          │
          ▼
         Gauge
          ▲
          │
    Data Collector
          ▲
          │
    Operating System
```

The exporter continuously collects information from the operating system and updates the metric values.

---

# Separation of Responsibilities

A Prometheus exporter has two independent responsibilities.

## Responsibility 1

Collect data.

Example:

```text
CPU Usage = 28%
```

The collector knows nothing about Prometheus.

Its only responsibility is reading data.

---

## Responsibility 2

Expose data.

Example:

```text
cpu_usage_percent 28
```

The Prometheus client knows nothing about how the CPU usage was collected.

It only exposes the current value through `/metrics`.

---

# Why This Separation Matters

Today we will collect data from the operating system.

Later lessons will replace the operating system with:

* Kubernetes API
* HTTP APIs
* Security Sensors
* Cloud Platforms

The exporter architecture remains exactly the same.

Only the data source changes.

---

# Hands-on Tasks

## Task 1 - Prediction

Consider the following code.

```python
while True:

    cpu = get_cpu()

    cpu_metric.set(cpu)

    time.sleep(5)
```

Predict:

1. How often is `get_cpu()` executed?
2. Does opening `/metrics` trigger `get_cpu()`?
3. Does Prometheus trigger `get_cpu()`?

Do not run any code yet.

Write your prediction first.

---

## Task 2 - Install psutil

Install the Python library used to read system information.

```bash
pip install psutil
```

Update the project dependencies.

```bash
pip freeze > requirements.txt
```

Observe:

* Installed version
* Installation path

---

## Task 3 - Read CPU Usage

Create a small Python program.

Read the current CPU usage using `psutil`.

Print the value every five seconds.

Do not use Prometheus yet.

Goal:

Understand how to collect system information independently of metrics.

---

## Task 4 - Read Memory Usage

Read:

* Total Memory
* Used Memory
* Available Memory
* Memory Usage Percentage

Print the values every five seconds.

Observe how they change when applications start or stop.

---

## Task 5 - Read Disk Usage

Read:

* Total Disk Size
* Used Disk Space
* Free Disk Space
* Disk Usage Percentage

Observe the values.

---

## Task 6 - Connect Data Collection to Prometheus

Create three Gauges.

```text
system_cpu_usage_percent

system_memory_usage_percent

system_disk_usage_percent
```

Update the Gauges using the values collected from `psutil`.

Expose them through:

```text
http://localhost:8000/metrics
```

Observe the values changing in real time.

---

## Task 7 - Observe the Architecture

While the exporter is running, answer:

1. Which component reads CPU usage?
2. Which component stores the metric value?
3. Which component exposes `/metrics`?
4. Does opening `/metrics` cause the operating system to be queried again?

Explain your reasoning.

---

# Knowledge Check

Answer these questions before moving to Lesson 04.

1. What is a data source?
2. Name five possible data sources for an exporter.
3. What are the two responsibilities of an exporter?
4. Why should data collection and metric exposure remain separate?
5. Which library did we use to collect system metrics?
6. Which component reads information from the operating system?
7. Which component stores the metric values?
8. Which component exposes the metrics?
9. If Prometheus stops scraping, does the exporter continue collecting data?
10. How will this architecture help us when we start reading data from Kubernetes instead of the operating system?

If you cannot confidently answer these questions, repeat the hands-on tasks before continuing.

---

# Next Lesson

In Lesson 04 we will replace the operating system with the Kubernetes API.

You'll learn:

* How the Kubernetes Python Client works
* Authentication methods
* In-cluster vs Out-of-cluster configuration
* Reading Pods, Nodes and Namespaces
* Preparing for the first Kubernetes exporter



# Polling Frequency

Our exporter currently collects system metrics using a simple loop.

```python
while True:
    collect_metrics()
    time.sleep(30)
```

This means the exporter:

1. Collects the metrics.
2. Sleeps for 30 seconds.
3. Repeats the process.

The actual time between two collections is:

```
Collection Time + Sleep Time
```

For example:

| Collection Time | Sleep Time | Actual Interval |
|-----------------|------------|-----------------|
| 1 second | 30 seconds | 31 seconds |
| 5 seconds | 30 seconds | 35 seconds |
| 10 seconds | 30 seconds | 40 seconds |

For this lesson, this simple approach is sufficient because collecting CPU, memory and disk information is very fast.

In later phases, when we collect information from Kubernetes, cloud providers and security platforms, we will improve this design so that the exporter maintains a consistent polling interval regardless of how long data collection takes.

The important takeaway is:

> **Choose the polling interval based on how frequently the data changes and how expensive it is to collect.**

Examples:

| Data Source | Recommended Polling Interval |
|--------------|-----------------------------|
| CPU Usage | 1–5 seconds |
| Memory Usage | 5–15 seconds |
| Disk Usage | 30–60 seconds |
| Kubernetes API | 30–60 seconds |
| Cloud APIs | 1–5 minutes |
| Security Platform APIs | 1–5 minutes |


# Key Takeaways

- An exporter collects data from a data source and exposes it through `/metrics`.
- `psutil` reads operating system information.
- `prometheus_client` exposes metrics to Prometheus.
- Data collection and metric exposure are separate responsibilities.
- CPU, memory and disk usage are different metrics and should have different metric names.
- Choose the polling interval based on how quickly the data changes and how expensive it is to collect.

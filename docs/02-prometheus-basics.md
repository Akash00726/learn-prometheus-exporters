# 02. Prometheus Basics

## Objective

By the end of this lesson, you will understand:

* What Prometheus is
* Why it was created
* How Prometheus collects metrics
* The pull model
* Time-series data
* Targets and exporters
* Prometheus architecture
* The complete metrics collection flow

---

# What is Prometheus?

Prometheus is an open-source monitoring system and time-series database.

Its primary responsibilities are to:

* Collect metrics
* Store metrics
* Query metrics
* Trigger alerts

It does **not** collect logs or traces.

---

# Why Was Prometheus Created?

Traditional monitoring systems often relied on agents pushing data to a central server.

This approach introduced problems:

* Complex agent management
* Firewall issues
* Duplicate data
* Difficult service discovery
* Scaling challenges

Prometheus simplified monitoring by introducing a pull-based architecture.

---

# What is a Metric?

A metric is a numerical measurement representing the state of a system at a specific point in time.

Examples:

| Metric        | Value |
| ------------- | ----: |
| CPU Usage     |    65 |
| Memory Usage  |    42 |
| Running Pods  |     8 |
| HTTP Requests | 1,245 |
| Disk Usage    |    71 |

Metrics are collected repeatedly.

---

# What is Time-Series Data?

A metric becomes valuable when it is collected over time.

Example:

| Time  | CPU |
| ----- | --: |
| 10:00 | 20% |
| 10:01 | 24% |
| 10:02 | 27% |
| 10:03 | 31% |
| 10:04 | 58% |

Instead of storing only the latest value, Prometheus stores every observation with a timestamp.

A single sample looks like:

```text
Timestamp: 10:03:00
Metric: cpu_usage
Value: 31
```

This is called **time-series data**.

---

# Prometheus Pull Model

Prometheus does not wait for applications to send data.

Instead, it periodically requests metrics from each target.

```text
          Every 15 Seconds

Prometheus
     |
     | HTTP GET /metrics
     |
     v
Application
```

This process is called **scraping**.

---

# What is Scraping?

Scraping means requesting metrics from an endpoint.

For example:

```text
GET http://localhost:8000/metrics
```

The application responds with metrics in Prometheus format.

Example:

```text
cpu_usage_percent 61
memory_usage_percent 48
requests_total 1502
```

Prometheus stores every value with a timestamp.

---

# What is a Target?

A target is anything Prometheus can scrape.

Examples:

* Python application
* Java application
* Kubernetes node
* Linux server
* Docker container
* Custom exporter

If it exposes a `/metrics` endpoint, it can become a target.

---

# What is an Exporter?

Many systems cannot expose Prometheus metrics natively.

An exporter acts as a translator.

```text
Database
     |
Reads statistics
     |
     v
Exporter
     |
Converts data
     |
     v
/metrics
     |
Prometheus
```

Examples:

* Node Exporter
* Blackbox Exporter
* MySQL Exporter
* PostgreSQL Exporter
* Kubernetes State Metrics

In this repository, you'll build your own exporter.

---

# Prometheus Architecture

```text
                 HTTP GET /metrics
                         |
                         |
                  +-------------+
                  | Prometheus  |
                  +------+------+ 
                         |
      +------------------+------------------+
      |                  |                  |
      v                  v                  v
+-------------+   +-------------+   +-------------+
| Exporter A  |   | Exporter B  |   | Application |
+-------------+   +-------------+   +-------------+
```

Prometheus can scrape hundreds or thousands of targets.

Each target exposes metrics independently.

---

# Storage

After scraping, Prometheus stores:

* Metric name
* Labels
* Value
* Timestamp

Example:

```text
Metric:
cpu_usage_percent

Labels:
instance="server01"

Timestamp:
2026-08-01T10:00:15

Value:
61
```

Together, these form a single time-series sample.

---

# Querying Metrics

Prometheus uses **PromQL (Prometheus Query Language)**.

Examples:

Return CPU metric:

```text
cpu_usage_percent
```

Return HTTP request count:

```text
http_requests_total
```

Average CPU:

```text
avg(cpu_usage_percent)
```

Later lessons will introduce PromQL in more detail.

---

# Complete Flow

```text
Application
      |
Generate statistics
      |
      v
Exporter
      |
Expose /metrics
      |
      | HTTP
      v
Prometheus
      |
Store time-series
      |
      v
Grafana
      |
Dashboards
```

This is the complete monitoring pipeline you'll build during this course.

---

# Common Misconceptions

### "Prometheus installs agents."

No.

Prometheus usually scrapes metrics over HTTP.

---

### "Grafana collects metrics."

No.

Grafana only visualizes data.

Prometheus collects and stores it.

---

### "Exporters store data."

No.

Exporters only expose metrics.

Prometheus stores them.

---

### "Prometheus monitors only Kubernetes."

No.

It can monitor:

* Linux
* Windows
* Kubernetes
* Docker
* Cloud services
* APIs
* Databases
* Network devices
* Custom applications

Anything capable of exposing metrics.

---

# Key Takeaways

* Prometheus is a monitoring system and time-series database.
* It uses a **pull model**.
* It collects metrics by scraping HTTP endpoints.
* A target is any system exposing metrics.
* Exporters convert application or system data into Prometheus metrics.
* Prometheus stores metric values along with timestamps and labels.
* Grafana visualizes metrics; it does not collect them.

---

# Next Lesson

In **03-exporter-basics.md**, you'll learn:

* What an exporter really is
* Why exporters exist
* The anatomy of a `/metrics` endpoint
* How the Python Prometheus client works internally
* What you'll build in Lesson 01

# 03. Exporter Basics

## Objective

By the end of this lesson, you will understand:

* What an exporter is
* Why exporters exist
* How a `/metrics` endpoint works
* The lifecycle of a Prometheus scrape
* The components of an exporter
* What you'll build in the next lesson

---

# What is an Exporter?

An exporter is a small application that collects information from another system and exposes it in the Prometheus metrics format.

Think of it as a translator.

```text
Application/System
        |
Reads data
        |
        v
+----------------+
|   Exporter     |
+----------------+
        |
Converts to Prometheus format
        |
        v
      /metrics
        |
        v
   Prometheus
```

The exporter **does not store data**.

It simply makes data available when Prometheus asks for it.

---

# Why Do Exporters Exist?

Most applications were not built with Prometheus support.

For example:

* A firewall
* A storage appliance
* A cloud API
* A security product
* A legacy application

These systems may expose:

* REST APIs
* JSON
* XML
* CLI commands
* SQL queries

Prometheus cannot understand these formats directly.

The exporter converts them into Prometheus metrics.

---

# Real Examples

| Exporter            | Reads From   | Exposes                    |
| ------------------- | ------------ | -------------------------- |
| Node Exporter       | Linux kernel | CPU, Memory, Disk, Network |
| MySQL Exporter      | MySQL        | Database metrics           |
| PostgreSQL Exporter | PostgreSQL   | Database metrics           |
| Blackbox Exporter   | HTTP/DNS/TCP | Availability metrics       |
| Custom Exporter     | Anything     | Anything you define        |

Our exporter will also be a **custom exporter**.

---

# What Does Prometheus Actually Request?

Prometheus simply performs an HTTP request.

```text
GET /metrics HTTP/1.1
Host: exporter:8000
```

The exporter returns plain text.

Example:

```text
cpu_usage_percent 67
memory_usage_percent 42
disk_usage_percent 71
```

That's it.

There is no special protocol.

Just HTTP and plain text.

---

# Inside an Exporter

Every exporter has the same basic workflow.

```text
        Request arrives
              |
              v
      Read current data
              |
              v
Generate metrics
              |
              v
Return response
```

Notice something important:

**Metrics are generated when Prometheus requests them.**

They are **not** continuously pushed.

---

# Exporter Lifecycle

Let's follow one scrape.

## Step 1

Prometheus sends:

```text
GET /metrics
```

---

## Step 2

The exporter starts collecting data.

For example:

```python
Read CPU

Read Memory

Read Disk
```

---

## Step 3

The exporter converts values into Prometheus metrics.

```text
cpu_usage_percent 68

memory_usage_percent 41

disk_usage_percent 72
```

---

## Step 4

The exporter returns the response.

Prometheus stores the values.

The exporter waits for the next request.

---

# Exporters Are Stateless

A good exporter should not maintain historical data.

Instead:

```text
Exporter

Current CPU = 61%

Return it
```

Five seconds later:

```text
Current CPU = 74%

Return it
```

Prometheus stores the history.

The exporter only knows the current state.

---

# Where Does the Data Come From?

An exporter can read data from almost anywhere.

```text
                Exporter
                    |
    +---------------+---------------+
    |               |               |
 REST API      Kubernetes API     Files
    |               |               |
    +---------------+---------------+
                    |
               Generate Metrics
```

Some exporters also read:

* Shell commands
* Databases
* Message queues
* Cloud SDKs
* YAML configuration
* SNMP
* TCP sockets

---

# Components of an Exporter

A production exporter is usually divided into logical components.

```text
                Exporter
                    |
    +---------------+---------------+
    |               |               |
Configuration   Data Collection   Metrics
                    |
                    v
              HTTP Server
```

We'll gradually build these pieces throughout this repository.

---

# The `/metrics` Endpoint

This endpoint is the contract between your exporter and Prometheus.

Every scrape returns the latest values.

Example:

```text
# HELP cpu_usage_percent CPU utilization percentage
# TYPE cpu_usage_percent gauge
cpu_usage_percent 67

# HELP memory_usage_percent Memory utilization percentage
# TYPE memory_usage_percent gauge
memory_usage_percent 41
```

The Python Prometheus client generates this format automatically.

You won't have to build it manually.

---

# One Request, One Response

A common misconception is that exporters continuously stream data.

They don't.

The interaction is simple.

```text
Prometheus
      |
GET /metrics
      |
      v
Exporter
      |
Collect current data
      |
Return metrics
      |
      v
Prometheus
```

After responding, the exporter becomes idle until the next scrape.

---

# Building Our Exporter

In this repository, we'll start small.

Lesson 1:

```text
+----------------+
| Python Script  |
+-------+--------+
        |
Generate one metric
        |
        v
     /metrics
```

Later, we'll expand it.

```text
+----------------------+
| Config Loader        |
+----------+-----------+
           |
+----------v-----------+
| Sensor Manager       |
+----------+-----------+
           |
+----------v-----------+
| Kubernetes Sensor    |
| HTTP Sensor          |
| Future Sensors...    |
+----------+-----------+
           |
+----------v-----------+
| Metrics Endpoint     |
+----------------------+
```

The architecture evolves naturally as the project grows.

---

# Key Takeaways

* An exporter translates data into Prometheus metrics.
* Prometheus pulls metrics using HTTP.
* Exporters are stateless.
* Exporters expose a `/metrics` endpoint.
* Prometheus stores historical data, not the exporter.
* Exporters can read data from APIs, databases, files, Kubernetes, or any external source.

---

# Next Lesson

In **Lesson 01 – Minimal Exporter**, you'll write your first exporter in fewer than 30 lines of Python.

You'll learn how to:

* Start a metrics server
* Create your first metric
* View the `/metrics` endpoint in a browser
* Understand what the Prometheus Python client generates automatically

From this point onward, every lesson will include runnable code, not just theory.

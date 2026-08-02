# Lesson 06 - YAML Configuration

## Objective

By the end of this lesson you will understand:

* Why configuration should be separated from application logic.
* Why YAML is the preferred configuration format in cloud-native applications.
* How to read YAML files in Python.
* How to replace hardcoded values with configuration.
* How to build configurable exporters instead of hardcoded scripts.

This lesson transforms our exporter from a learning script into a configurable application.

---

# Looking Back

Our exporter currently works correctly.

It:

* Connects to Kubernetes.
* Counts Running Pods.
* Updates Prometheus metrics.
* Exposes `/metrics`.

However, everything is hardcoded.

Example:

```python
start_http_server(8000)

time.sleep(30)
```

Question:

What happens if another engineer wants:

* Port 9090?
* Poll every 60 seconds?
* Poll every 10 seconds?

Currently, they must edit Python code.

That is not how production software is built.

---

# The Problem

Current exporter:

```text
Python Code

│

├── Port = 8000
├── Poll Interval = 30
├── Monitor All Namespaces
└── Metric Configuration
```

Every configuration change requires:

```text
Edit Code

↓

Commit

↓

Review

↓

Deploy
```

Even though the application logic never changes.

---

# Configuration vs Logic

Application logic answers:

> **What should the program do?**

Example:

* Connect to Kubernetes
* Count Running Pods
* Update Prometheus metrics

Configuration answers:

> **How should the program behave?**

Example:

* Which port?
* Poll every how many seconds?
* Which namespaces?
* Which metrics?

Logic should remain stable.

Configuration should change easily.

---

# Why YAML?

Cloud-native technologies commonly use YAML.

Examples:

* Kubernetes
* Argo CD
* Helm
* Docker Compose
* GitHub Actions
* Prometheus
* Grafana

Learning YAML once allows you to work comfortably across the cloud-native ecosystem.

---

# Why Not Hardcode Values?

Hardcoded:

```python
start_http_server(8000)

time.sleep(30)
```

Configurable:

```python
start_http_server(config["server"]["port"])

time.sleep(config["exporter"]["poll_interval"])
```

Notice something.

The application logic did not change.

Only the source of the values changed.

---

# First Configuration File

Create:

```text
config.yaml
```

Example:

```yaml
server:
  port: 8000

exporter:
  poll_interval: 30
```

Simple.

Only two values.

We will gradually expand this configuration throughout the remaining lessons.

---

# How Configuration Flows

```text
config.yaml
        │
        ▼
PyYAML
        │
        ▼
Python Dictionary
        │
        ▼
Exporter
        │
        ▼
Application Behavior
```

Notice the similarity with previous lessons.

Lesson 03

```text
Linux

↓

psutil

↓

Python Objects
```

Lesson 04

```text
Kubernetes

↓

Python Client

↓

Python Objects
```

Lesson 06

```text
YAML

↓

PyYAML

↓

Python Dictionary
```

Every lesson follows the same pattern.

External data is converted into Python objects that our application can use.

---

# Why YAML Instead of JSON?

YAML is easier for humans to read and edit.

Example:

JSON

```json
{
  "server": {
    "port": 8000
  },
  "exporter": {
    "poll_interval": 30
  }
}
```

YAML

```yaml
server:
  port: 8000

exporter:
  poll_interval: 30
```

YAML is cleaner and is the standard configuration format in Kubernetes.

---

# Architecture Evolution

Previous Lesson

```text
Exporter

│

├── Hardcoded Port
├── Hardcoded Interval
└── Hardcoded Settings
```

Current Lesson

```text
Exporter
        ▲
        │
Configuration
(config.yaml)
```

The exporter now depends on configuration rather than hardcoded values.

---

# Hands-on Labs

## Lab 1

Create the first YAML configuration file.

---

## Lab 2

Read YAML using PyYAML.

---

## Lab 3

Understand how YAML becomes a Python dictionary.

---

## Lab 4

Replace the hardcoded HTTP port.

---

## Lab 5

Replace the hardcoded polling interval.

---

## Lab 6

Verify that changing only YAML changes exporter behavior without modifying Python code.

---

# Knowledge Check

By the end of this lesson you should be able to answer:

1. What is the difference between configuration and application logic?
2. Why should configuration live outside the code?
3. Why is YAML widely used in cloud-native technologies?
4. What Python object does PyYAML return?
5. Why is configuration easier to maintain than hardcoded values?
6. What are the advantages of changing YAML instead of Python?

---

# Key Takeaways

* Production software separates configuration from logic.
* YAML is the standard configuration format in Kubernetes and cloud-native systems.
* PyYAML converts YAML into Python dictionaries.
* Configuration should change without modifying application code.
* Good software becomes configurable before it becomes extensible.

---

# Next Lesson

In Lesson 07 we will extend the exporter to support **multiple sensors**.

Instead of collecting only Kubernetes Pod information, our exporter will be able to collect data from multiple independent sensors using the same configuration-driven framework.

This is the first major step toward building our Security Observability Platform.

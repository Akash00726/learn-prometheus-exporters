# Security Observability Platform

> Learn how to build a custom Prometheus exporter from scratch and evolve it into a reusable Security Observability Platform.

---

# Goal

This repository is **not** a collection of scripts.

The goal is to understand **how a custom exporter works internally** by building one step by step.

By the end of this project, you should be able to build exporters for any data source, including:

- Kubernetes
- Linux
- REST APIs
- AWS
- Azure
- GCP
- Databases
- Security tools such as Falco, Trivy, Kubescape, Wiz, Vault, etc.

The focus is on **understanding the concepts**, not memorizing code.

---

# Target Audience

This project assumes you:

- Know basic Python
- Understand variables, loops, functions and modules
- Have little or no knowledge of Prometheus exporters
- Want to understand **why** each component exists
- Prefer building from scratch instead of using frameworks

---

# Final Objective

We will build a reusable exporter that can monitor multiple security tools simply by changing configuration.

Example:

```
Falco
      │
      ▼
Trivy
      │
      ▼
Kubescape
      │
      ▼
Vault
      │
      ▼
Security Observability Platform
      │
      ▼
Prometheus
      │
      ▼
Grafana
```

---

# Learning Philosophy

We will **not** start with a complex architecture.

Instead, we will continuously improve the exporter.

Every lesson answers one question:

> "What problem are we trying to solve?"

Only after experiencing that problem will we introduce a new component.

---

# What is a Custom Exporter?

A custom exporter is a small application whose only responsibility is to:

1. Read data from a source.
2. Convert it into Prometheus metrics.
3. Expose those metrics through an HTTP endpoint.

That's all.

An exporter is **not**

- a database
- a monitoring system
- an alert manager
- a dashboard

It is simply a translator.

```
Data Source

      │

      ▼

Read Data

      │

      ▼

Convert to Metrics

      │

      ▼

Expose /metrics
```

---

# Exporter Responsibilities

Our exporter will perform four jobs.

## 1. Read Information

Example:

- Kubernetes Pods
- HTTP Endpoint
- Linux Process
- REST API

---

## 2. Evaluate Health

Example:

```
Are all pods running?

Yes

↓

Healthy
```

or

```
One pod failed

↓

Unhealthy
```

---

## 3. Generate Metrics

Example:

```
falco_health 1

vault_health 1

trivy_health 0
```

---

## 4. Expose Metrics

The exporter exposes an endpoint.

```
GET /metrics
```

Prometheus reads this endpoint periodically.

---

# High-Level Architecture

```
                Data Source

                     │

                     ▼

              Custom Exporter

                     │

          ┌──────────┴──────────┐

          │                     │

    Health Evaluation     Metric Generation

          │                     │

          └──────────┬──────────┘

                     ▼

                 /metrics

                     │

                     ▼

                Prometheus

                     │

                     ▼

                 Grafana
```

---

# Components We Will Build

We are not starting with all components.

Each one will be introduced only when needed.

| Component | Responsibility |
|-----------|----------------|
| app.py | HTTP server |
| collector.py | Collect data |
| metrics.py | Generate Prometheus metrics |
| loader.py | Read configuration |
| scheduler.py | Execute checks periodically |
| providers | Read data from external systems |
| plugins | Implement health checks |

---

# Why Do These Components Exist?

## app.py

Responsible for serving HTTP requests.

Without it, Prometheus has nothing to query.

---

## collector.py

Coordinates the entire workflow.

```
Read

↓

Check

↓

Publish
```

---

## metrics.py

Knows how Prometheus expects metrics to look.

Other modules should not care about metric formatting.

---

## loader.py

Reads configuration.

Initially we won't need this.

Later it allows adding new sensors without modifying Python code.

---

## scheduler.py

Runs health checks periodically.

Without it, data would only be collected when someone requests `/metrics`.

---

## providers/

Providers know **how to retrieve information**.

Examples:

```
Kubernetes Provider

↓

Read Pods
```

or

```
HTTP Provider

↓

Call REST API
```

---

## plugins/

Plugins know **how to evaluate health**.

Example:

```
Pods

↓

Are all Running?

↓

Healthy
```

Notice the difference.

Providers fetch data.

Plugins interpret data.

---

# How Everything Works Together

```
            Request

               │

               ▼

           app.py

               │

               ▼

         collector.py

               │

               ▼

          providers/

               │

               ▼

        External System

               │

               ▼

          plugins/

               │

               ▼

          metrics.py

               │

               ▼

          HTTP Response
```

---

# Development Roadmap

We will build the exporter in small milestones.

## Phase 1

Understand the smallest exporter possible.

Topics

- HTTP server
- /metrics
- Hardcoded metric

---

## Phase 2

Replace hardcoded values with Python logic.

Topics

- Variables
- Functions
- Health evaluation

---

## Phase 3

Read real data.

Topics

- Kubernetes Python Client
- Listing Pods
- Reading Deployments

---

## Phase 4

Generate real Prometheus metrics.

Topics

- Gauges
- Labels
- Metric naming

---

## Phase 5

Support multiple sensors.

Topics

- Configuration
- YAML
- Dynamic loading

---

## Phase 6

Refactor into a reusable framework.

Topics

- Providers
- Plugins
- Scheduler
- Extensibility

---

# Repository Philosophy

The objective of this repository is not to create the most feature-rich exporter.

The objective is to understand **how exporters are designed** so that you can build your own for any platform or security product.

By the end of this journey, you should be able to answer:

- How does an exporter work?
- Why are exporters designed this way?
- How do I monitor a new system?
- How do I design my own exporter?
- How do I make it reusable?
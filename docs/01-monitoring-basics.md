# 01. Monitoring Basics

## Objective

By the end of this lesson, you will understand:

* Why monitoring exists
* What problems monitoring solves
* The difference between monitoring and logging
* The four golden signals
* Why metrics are preferred for health monitoring
* How Prometheus fits into the monitoring ecosystem

---

# What is Monitoring?

Monitoring is the continuous process of observing the health, performance, and availability of a system.

Think of monitoring as a dashboard in a car.

While driving, you don't stop every few minutes to check the engine. Instead, you continuously watch:

* Speed
* Fuel level
* Engine temperature
* Battery warning
* Oil pressure

If something becomes abnormal, the dashboard immediately tells you.

Software systems work the same way.

Instead of manually checking servers, applications, or Kubernetes clusters, monitoring continuously collects data and alerts us when something goes wrong.

---

# Why Do We Need Monitoring?

Imagine an API server.

```
Users
   |
   v
Application
   |
Database
```

Without monitoring:

* You don't know if the application is running.
* You don't know whether users can access it.
* You don't know if CPU usage is 20% or 100%.
* You don't know whether memory is exhausted.
* You don't know if requests are taking 50 ms or 5 seconds.

Monitoring answers these questions continuously.

---

# Real-World Example

Imagine a Kubernetes cluster with 50 applications.

One application suddenly becomes unavailable.

Without monitoring:

* Users report the problem.
* Engineers investigate manually.
* Root cause analysis begins after the outage.

With monitoring:

* CPU spike detected.
* Memory usage increasing.
* Pod restarting repeatedly.
* Alert generated immediately.

Engineers begin troubleshooting before many users are affected.

Monitoring reduces detection time dramatically.

---

# Monitoring vs Logging

These two concepts are often confused.

## Monitoring

Monitoring answers:

> "Is the system healthy?"

Examples:

* CPU usage
* Memory usage
* Disk usage
* Network traffic
* Number of running Pods
* HTTP request rate

Monitoring is based primarily on **metrics**.

---

## Logging

Logging answers:

> "What exactly happened?"

Example log:

```
2026-08-01 10:21:13
Database connection failed.
Timeout after 30 seconds.
```

Logs contain detailed events.

You investigate logs **after** monitoring tells you something is wrong.

---

## Relationship

```
Problem occurs
       |
       v
 Monitoring detects abnormal behaviour
       |
       v
 Alert generated
       |
       v
 Engineer investigates logs
       |
       v
 Root cause identified
```

Monitoring tells you **where** to look.

Logs tell you **what** happened.

---

# Monitoring vs Alerting

Monitoring collects data.

Alerting acts on that data.

Example:

Metric:

```
CPU Usage = 95%
```

Alert rule:

```
If CPU > 90% for 5 minutes
Send alert
```

Monitoring and alerting are different responsibilities.

---

# The Four Golden Signals

Google's Site Reliability Engineering (SRE) defines four key indicators for service health.

## 1. Latency

How long does a request take?

Example:

```
Login API

Average Response Time

45 ms
```

High latency usually indicates performance issues.

---

## 2. Traffic

How much work is the system handling?

Examples:

* Requests per second
* Active users
* API calls

Traffic helps you understand workload.

---

## 3. Errors

How many requests are failing?

Example:

```
200 OK

95%

500 Internal Server Error

5%
```

An increase in errors usually indicates a service problem.

---

## 4. Saturation

How close is the system to its capacity?

Examples:

* CPU 95%
* Memory 92%
* Disk full
* Network bandwidth exhausted

High saturation often leads to failures.

---

# Types of Monitoring Data

Modern monitoring generally uses three types of telemetry.

## Metrics

Small numerical values.

Examples:

```
CPU = 72%

Memory = 58%

Pods Running = 15
```

Metrics are lightweight and ideal for dashboards and alerts.

---

## Logs

Detailed event records.

Example:

```
User login failed
Authentication timeout
```

Useful for troubleshooting.

---

## Traces

Show the path of a request through multiple services.

Example:

```
Browser
   |
API Gateway
   |
Authentication Service
   |
User Service
   |
Database
```

Useful in distributed systems.

---

# Why Metrics Are So Important

Metrics are:

* Fast to collect
* Small in size
* Easy to aggregate
* Easy to graph
* Ideal for alerting

This is why Prometheus is built around metrics.

---

# Where Prometheus Fits

```
Application
      |
      | exposes metrics
      v
+------------------+
|    Prometheus    |
+------------------+
        |
Stores time-series data
        |
        v
+------------------+
|     Grafana      |
+------------------+
        |
Dashboards & Alerts
```

Prometheus does not display beautiful dashboards.

Its job is to collect, store, and query metrics.

Grafana visualizes those metrics.

---

# Key Takeaways

* Monitoring continuously observes system health.
* Monitoring is different from logging.
* Metrics answer **"How is the system performing?"**
* Logs answer **"What happened?"**
* Alerting reacts to monitoring data.
* The four golden signals are Latency, Traffic, Errors, and Saturation.
* Prometheus is a metrics collection and storage system.

---

# Next Lesson

In **02-prometheus-basics.md**, you'll learn:

* What Prometheus is
* Why it uses a pull model
* Time-series databases
* Scraping
* Targets
* Exporters
* Prometheus architecture

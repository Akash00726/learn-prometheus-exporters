# Lesson 01 - Minimal Exporter

## Objective

Build a working Prometheus exporter from scratch.

By the end of this lesson you will:

* Install the Prometheus Python client
* Start a metrics HTTP server
* Create your first metric
* Watch Prometheus scrape it (later)
* Understand every line of the code

---

# Step 1 - Create the Lesson Directory

```
lessons/
└── lesson-01-minimal-exporter/
    └── exporter.py
```

---

# Step 2 - Install Dependencies

From the repository root:

```bash
pip install prometheus_client
```

or

```bash
pip install -r requirements.txt
```

Later we'll populate `requirements.txt`.

---

# Step 3 - Write the Exporter

Create `exporter.py`

```python
from prometheus_client import Gauge, start_http_server
import time

cpu_temperature = Gauge(
    "cpu_temperature_celsius",
    "Current CPU temperature"
)

start_http_server(8000)

print("Exporter running on http://localhost:8000/metrics")

temperature = 40

while True:
    temperature += 1

    if temperature > 80:
        temperature = 40

    cpu_temperature.set(temperature)

    print(f"Temperature: {temperature}")

    time.sleep(2)
```

Save the file.

---

# Step 4 - Run It

```bash
python exporter.py
```

Output:

```
Exporter running on http://localhost:8000/metrics

Temperature: 41
Temperature: 42
Temperature: 43
...
```

The exporter is now running.

---

# Step 5 - Open the Metrics Endpoint

Open your browser.

```
http://localhost:8000/metrics
```

You will see many metrics.

Some belong to Python.

One belongs to us.

```
cpu_temperature_celsius 45
```

Congratulations.

You have written your first Prometheus exporter.

---

# Wait...

We only created one metric.

Why are there dozens of metrics?

Example:

```
python_gc_objects_collected_total

process_cpu_seconds_total

process_virtual_memory_bytes

python_info

...
```

Those are automatically exposed by the Prometheus Python client.

They provide useful runtime information about your exporter.

---

# Understanding the Code

Let's examine every line.

---

## Import

```python
from prometheus_client import Gauge, start_http_server
```

We imported two things.

`Gauge`

Represents a metric whose value can increase or decrease.

Examples:

* CPU usage
* Memory usage
* Temperature
* Active sessions

---

`start_http_server`

Creates a tiny web server.

Without writing Flask or FastAPI.

It automatically exposes:

```
/metrics
```

---

## Import Time

```python
import time
```

Used only to pause the loop.

Without it, the loop would run millions of times per second.

---

## Create a Gauge

```python
cpu_temperature = Gauge(
    "cpu_temperature_celsius",
    "Current CPU temperature"
)
```

This creates a metric.

Metric name

```
cpu_temperature_celsius
```

Description

```
Current CPU temperature
```

Prometheus stores both.

---

## Start the HTTP Server

```python
start_http_server(8000)
```

This starts an HTTP server.

Port

```
8000
```

Endpoint

```
/metrics
```

Equivalent URL

```
http://localhost:8000/metrics
```

You didn't write any HTTP code.

The library handled it.

---

## Initialize Data

```python
temperature = 40
```

A fake temperature.

Later this will come from:

* Linux
* Kubernetes
* REST APIs
* Sensors

Today we're just simulating data.

---

## Infinite Loop

```python
while True:
```

Real exporters run continuously.

They don't exit after one execution.

---

## Change the Value

```python
temperature += 1
```

Simulate changing data.

Real exporters would instead do something like:

```python
temperature = read_sensor()
```

---

## Reset

```python
if temperature > 80:
    temperature = 40
```

Keeps the demo repeating.

---

## Update the Metric

```python
cpu_temperature.set(temperature)
```

This is the most important line.

It tells Prometheus:

```
Current value = 56
```

Every scrape reads the latest value.

---

## Wait

```python
time.sleep(2)
```

Without this,

```
40
41
42
43
...
```

would happen millions of times per second.

---

# What Happens Internally?

```
Program starts
        |
        v
Create Gauge
        |
        v
Start HTTP Server
        |
        v
Loop Forever
        |
        +---------------------------+
        |                           |
        | Update Metric             |
        |                           |
        +-------------+-------------+
                      |
                      v
        Prometheus requests /metrics
                      |
                      v
Current value returned
```

Notice something important.

The HTTP server and your loop run independently.

Your loop updates the metric.

The HTTP server simply returns its current value whenever Prometheus asks.

---

# Exercise

Modify the program.

Instead of temperature,

create a metric called

```
students_online
```

Start at

```
15
```

Increase it every two seconds.

Reset to

```
15
```

after reaching

```
40
```

Don't worry about Prometheus yet.

Just make the metric appear at

```
/metrics
```

---

# What You Learned

You now know how to:

* Create a Prometheus metric
* Start a metrics server
* Update metric values
* Expose a `/metrics` endpoint
* Run a basic exporter

Most importantly, you've built the core of every Prometheus exporter.

Everything else in this repository builds on this foundation.


# 04. Prometheus Metrics

## Objective

By the end of this lesson you will understand:

* What a metric is
* The four Prometheus metric types
* When to use each type
* Which metric types we'll use in our exporter

---

# What is a Metric?

A metric is a numerical measurement describing the current state of something.

Examples:

| Metric            |  Value |
| ----------------- | -----: |
| CPU Usage         |     68 |
| Memory Usage      |     42 |
| Running Pods      |     15 |
| Failed Logins     |     27 |
| API Response Time | 125 ms |

Prometheus periodically stores these values with timestamps.

---

# Metric Naming Convention

Metric names should clearly describe what they measure.

Good examples:

```text
cpu_usage_percent

memory_usage_bytes

disk_free_bytes

http_requests_total

api_response_seconds
```

Bad examples:

```text
cpu

metric1

test

value
```

A metric name should answer:

> "What exactly am I measuring?"

---

# The Four Metric Types

Prometheus provides four metric types.

```text
Metrics
   |
   +-- Gauge
   |
   +-- Counter
   |
   +-- Histogram
   |
   +-- Summary
```

Each serves a different purpose.

---

# 1. Gauge

A Gauge represents a value that can increase **or decrease**.

Examples:

* CPU usage
* Memory usage
* Temperature
* Running Pods
* Queue length
* Active users

Example:

```text
CPU

65
67
62
58
71
69
```

The value moves up and down.

Python:

```python
from prometheus_client import Gauge

cpu_usage = Gauge(
    "cpu_usage_percent",
    "Current CPU usage"
)

cpu_usage.set(72)
```

---

## When to Use Gauge

Use a Gauge whenever the current value can move in either direction.

Typical exporter metrics:

```text
sensor_health

disk_usage_percent

memory_usage

temperature

running_containers

running_pods
```

Our exporter will mostly use Gauges.

---

# 2. Counter

A Counter only increases.

It never decreases.

Examples:

* Requests served
* Failed logins
* Errors
* Files processed

Example:

```text
10
15
21
32
48
49
50
```

Notice it never goes backwards.

Python:

```python
from prometheus_client import Counter

requests = Counter(
    "http_requests_total",
    "Total HTTP requests"
)

requests.inc()
```

Increase by 5:

```python
requests.inc(5)
```

---

## When to Use Counter

Good examples:

```text
api_requests_total

errors_total

emails_sent_total

jobs_completed_total
```

Notice the `_total` suffix.

This is the Prometheus naming convention for counters.

---

# 3. Histogram

Histograms measure distributions.

Imagine recording API response times.

```text
120 ms
90 ms
180 ms
220 ms
95 ms
```

Instead of storing every value separately, Prometheus groups them into buckets.

Example:

```text
<=100 ms

45 requests

<=250 ms

98 requests

<=500 ms

110 requests
```

Histograms help answer questions like:

* How many requests finished within 100 ms?
* What percentage finished under 500 ms?
* Are response times getting slower?

Python:

```python
from prometheus_client import Histogram

response_time = Histogram(
    "http_response_seconds",
    "Response time"
)

response_time.observe(0.42)
```

---

# 4. Summary

A Summary also records observations.

Example:

```text
120 ms
110 ms
130 ms
105 ms
```

It calculates statistical values such as:

* Average
* Total
* Count

Python:

```python
from prometheus_client import Summary

request_time = Summary(
    "request_duration_seconds",
    "Request duration"
)

request_time.observe(0.25)
```

---

# Histogram vs Summary

This is a common interview question.

| Histogram                             | Summary             |
| ------------------------------------- | ------------------- |
| Uses buckets                          | No buckets          |
| Good for aggregating across instances | Limited aggregation |
| Preferred in Prometheus ecosystems    | Less commonly used  |

Most exporters use **Histogram**.

---

# Which Metrics Will Our Exporter Use?

Imagine monitoring Kubernetes sensors.

| Metric               | Type      |
| -------------------- | --------- |
| Sensor healthy       | Gauge     |
| Sensor response time | Histogram |
| Sensor API requests  | Counter   |
| Exporter uptime      | Gauge     |

Most infrastructure exporters primarily use Gauges and Counters.

---

# Example Exporter Metrics

Imagine a security exporter.

```text
sensor_up

1
```

Meaning:

The sensor is healthy.

---

```text
sensor_response_time_seconds

0.37
```

---

```text
sensor_requests_total

1523
```

---

```text
sensor_errors_total

12
```

These names are descriptive, predictable, and follow Prometheus conventions.

---

# Labels

Metrics become much more useful when combined with labels.

Example:

```text
sensor_up{name="wiz"} 1

sensor_up{name="prisma"} 1

sensor_up{name="crowdstrike"} 0
```

Instead of creating separate metrics, one metric can describe many resources.

We'll introduce labels in detail after building the basic exporter.

---

# Common Mistakes

Using a Gauge for request count.

Incorrect:

```text
requests
```

Correct:

```text
requests_total
```

---

Using a Counter for CPU usage.

Incorrect:

```text
cpu_usage_total
```

Correct:

```text
cpu_usage_percent
```

CPU usage changes constantly.

It is not cumulative.

---

Creating a separate metric for every object.

Incorrect:

```text
pod1_cpu

pod2_cpu

pod3_cpu
```

Correct:

```text
pod_cpu_usage{pod="pod1"}

pod_cpu_usage{pod="pod2"}

pod_cpu_usage{pod="pod3"}
```

Labels are the correct solution.

---

# Summary

| Metric Type | Can Decrease? | Typical Use         |
| ----------- | ------------- | ------------------- |
| Gauge       | Yes           | CPU, Memory, Status |
| Counter     | No            | Requests, Errors    |
| Histogram   | Buckets       | Latency             |
| Summary     | Statistics    | Latency             |

---

# What We'll Use

In this repository:

* **Gauge** → Current health and status
* **Counter** → API calls and errors
* **Histogram** → Response time
* **Summary** → Mentioned for completeness, but not used in our exporter

This mirrors what you'll see in production-grade exporters.

---

# Next Lesson

We'll stop writing toy metrics and start collecting **real data**.

Instead of generating fake temperatures, the exporter will read actual system information from Python and expose it as Prometheus metrics.

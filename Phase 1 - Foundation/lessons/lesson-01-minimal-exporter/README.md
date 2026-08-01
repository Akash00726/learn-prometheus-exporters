# Lesson 01 - Minimal Prometheus Exporter

## Objective

In this lesson you will learn how to:

* Start a Prometheus metrics server
* Create your first metric
* Understand how the `/metrics` endpoint works
* Observe auto-generated metrics
* Understand the relationship between your Python application and Prometheus

**We will NOT learn Counter, Histogram, Labels, or Prometheus scraping yet.**

---

# Theory

A Prometheus exporter is simply a program that exposes metrics over HTTP.

The exporter does **not** push metrics to Prometheus.

Instead, it waits for someone to request:

```text
http://localhost:8000/metrics
```

When that request arrives, the exporter returns the latest values of all available metrics.

In this lesson, there is no Prometheus server.

You will directly access the `/metrics` endpoint from your browser.

---

# Hands-on Tasks

## Task 1 - Install the Prometheus Client

Install the Python library.

```bash
pip install prometheus_client
```

Verify the installation.

```bash
pip show prometheus_client
```

### Observe

* Installed version
* Installation path

---

## Task 2 - Start the Smallest Exporter

Create a file named:

```text
exporter.py
```

Paste the following code.

```python
from prometheus_client import start_http_server

start_http_server(8000)

print("Exporter Started")

while True:
    pass
```

Run it.

```bash
python exporter.py
```

### Observe

Open your browser.

```
http://localhost:8000/metrics
```

### Questions

1. Does the page open?
2. We never used Flask or FastAPI. Who created the HTTP server?
3. What is the purpose of `start_http_server()`?

Do not continue until you understand this.

---

## Task 3 - Observe the Metrics

Scroll through the `/metrics` page.

You should notice many metrics beginning with:

```text
python_
```

and

```text
process_
```

### Questions

1. Did we create these metrics?
2. Why are they available?
3. What information do they appear to represent?

Do not worry about understanding every metric yet.

Simply observe them.

---

## Task 4 - Create Your First Metric

Replace the code with:

```python
from prometheus_client import Gauge, start_http_server

temperature = Gauge(
    "temperature",
    "Room Temperature"
)

start_http_server(8000)

temperature.set(25)

while True:
    pass
```

Run the exporter again.

Refresh:

```
http://localhost:8000/metrics
```

Search for:

```text
temperature
```

### Questions

1. Can you find the metric?
2. What value does it contain?
3. Did Python create the value?
4. Did Prometheus create the value?

---

## Task 5 - Change the Metric Value

Modify:

```python
temperature.set(25)
```

to

```python
temperature.set(50)
```

Restart the exporter.

Refresh the browser.

### Questions

1. Did the metric value change?
2. What changed?
3. Who stores the value?

---

## Task 6 - Update the Metric Continuously

Replace the code after `start_http_server()` with:

```python
import time

value = 20

while True:

    temperature.set(value)

    print(value)

    value += 1

    if value > 40:
        value = 20

    time.sleep(1)
```

Refresh the browser several times.

### Observe

The metric value changes every second.

### Questions

1. Is the browser calculating the value?
2. Is Prometheus calculating the value?
3. Who owns the current metric value?

---

## Task 7 - Understand the Metric Format

Locate the following lines:

```text
# HELP temperature Room Temperature

# TYPE temperature gauge

temperature 27
```

### Questions

What do these lines represent?

* `# HELP`
* `# TYPE`
* `temperature 27`

Do not memorize them.

Try to understand their purpose.

---

## Task 8 - Add Another Metric

Create another Gauge.

Suggested metric:

```text
humidity
```

Assign any value.

Example:

```text
humidity = 65
```

Refresh `/metrics`.

### Observe

You should now have two custom metrics.

### Questions

1. How many `/metrics` endpoints exist?
2. How many custom metrics exist?
3. Can one endpoint expose multiple metrics?

---

## Task 9 - Mini Exercise

Without copying previous code, create a metric named:

```text
cpu_usage
```

Requirements:

* Initial value: 10
* Increase every second
* Reset to 10 after reaching 100

If you can complete this task without referring back to earlier examples, you've understood the basic exporter workflow.

---

# Knowledge Check

Before moving to Lesson 02, answer these questions in your own words.

1. What does `start_http_server()` do?
2. Why didn't we need Flask or FastAPI?
3. What is a Gauge?
4. Who owns the metric value?
5. What is `/metrics`?
6. Why are `python_*` metrics available automatically?
7. What is the purpose of `# HELP`?
8. What is the purpose of `# TYPE`?
9. Can one exporter expose multiple metrics?
10. At this stage, is Prometheus involved anywhere?

If you cannot answer these comfortably, repeat the tasks before continuing.

---

# Next Lesson

Move to **Lesson 02** only after:

* You have completed all hands-on tasks.
* You understand the answers to the Knowledge Check.
* You are comfortable reading the `/metrics` output.

In Lesson 02, we will introduce:

* Gauge
* Counter
* Histogram
* Labels
* When to use each metric type

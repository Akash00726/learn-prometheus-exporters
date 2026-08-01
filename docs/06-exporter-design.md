# 06. Exporter Design

## Objective

By the end of this lesson, you will understand:

* Why exporter architecture matters
* How to design an extensible exporter
* Separation of responsibilities
* Sensor-based architecture
* Configuration-driven design
* The architecture we'll build in this repository

---

# Why Exporter Design Matters

A simple exporter may start with only 30 lines of code.

Example:

```python
while True:
    cpu = get_cpu_usage()
    cpu_metric.set(cpu)
```

This is fine for learning.

But what happens when you need to monitor:

* Kubernetes
* HTTP APIs
* Wiz
* Prisma Cloud
* Azure
* AWS
* Databases

Putting everything into one file quickly becomes difficult to maintain.

Good architecture allows the exporter to grow without becoming harder to understand.

---

# A Poor Design

Many beginners write exporters like this:

```text
exporter.py

├── Read YAML
├── Connect Kubernetes
├── Call REST API
├── Calculate Metrics
├── Handle Errors
├── Start HTTP Server
├── Expose Metrics
└── Main Loop
```

Problems:

* One very large file
* Difficult to test
* Difficult to extend
* Difficult to debug
* Every new feature modifies the same file

As the exporter grows, so does technical debt.

---

# A Better Design

Instead, separate responsibilities.

```text
Exporter
    │
    ├── Configuration
    ├── Sensors
    ├── Metrics
    ├── HTTP Server
    └── Main Loop
```

Each component has one responsibility.

---

# Separation of Responsibilities

## Configuration

Responsible for:

* Reading YAML
* Validation
* Default values

It should **not** collect metrics.

---

## Sensors

Responsible for collecting data.

Examples:

* Kubernetes
* HTTP API
* Local system
* Cloud platform

A sensor does **not** expose metrics directly.

It only returns data.

---

## Metrics

Responsible for:

* Creating Prometheus metrics
* Updating metric values
* Labels
* Metric naming

It does **not** know where the data came from.

---

## HTTP Server

Responsible for:

* Serving `/metrics`

Nothing else.

---

## Main Loop

Responsible for:

* Calling sensors
* Updating metrics
* Scheduling

Nothing else.

---

# Sensor-Based Architecture

A sensor represents one source of information.

```text
Exporter
     │
     ├── Kubernetes Sensor
     ├── HTTP Sensor
     ├── Azure Sensor
     ├── AWS Sensor
     └── Wiz Sensor
```

Every sensor follows the same pattern.

```text
Collect Data
      │
      ▼
Return Dictionary
```

Example:

```python
{
    "healthy": True,
    "response_time": 0.23
}
```

The sensor does **not** create Prometheus metrics.

It simply reports observations.

---

# Why Keep Sensors Independent?

Imagine replacing one sensor.

```text
Old

Kubernetes Sensor
```

with

```text
Wiz Sensor
```

Nothing else should change.

The metrics layer still receives data.

The HTTP server still exposes metrics.

The configuration still works.

This is called **loose coupling**.

---

# Configuration-Driven Design

The exporter should not require code changes to monitor different systems.

Instead, behavior should come from configuration.

Example:

```yaml
sensors:
  - type: kubernetes
    enabled: true

  - type: http
    enabled: true
```

Changing configuration changes behavior.

No Python code needs modification.

---

# Scope Awareness

Earlier we discussed namespace and cluster monitoring.

Instead of embedding that logic inside every sensor:

❌ Bad

```text
Kubernetes Sensor

if cluster...

if namespace...

if namespaces...
```

A better approach is:

```text
Configuration
      │
      ▼
Scope Manager
      │
      ▼
Sensor
```

The sensor receives its scope from configuration.

It simply collects data.

This keeps the sensor focused on one responsibility.

---

# Proposed Architecture

```text
                    +----------------------+
                    |   exporter.py        |
                    +----------+-----------+
                               |
                               |
                +--------------+--------------+
                |                             |
         Configuration                 Metric Manager
                |                             |
                |                             |
         Scope Manager                Prometheus Client
                |
      +---------+---------+
      |         |         |
      |         |         |
 Kubernetes   HTTP      Future Sensors
    Sensor    Sensor
```

Every component has a clearly defined responsibility.

---

# Data Flow

```text
Configuration
      │
      ▼
Load Sensors
      │
      ▼
Collect Data
      │
      ▼
Metric Manager
      │
      ▼
Prometheus Metrics
      │
      ▼
HTTP Server
      │
      ▼
Prometheus
```

Notice that sensors never communicate directly with Prometheus.

---

# Project Structure

By the end of this repository, the exporter will look similar to:

```text
final-project/

├── exporter.py
├── config.py
├── metrics.py
├── scope.py
├── collector.py
├── sensors/
│   ├── base.py
│   ├── kubernetes.py
│   ├── http.py
│   └── wiz.py
│
├── config/
│   └── sensors.yaml
│
└── requirements.txt
```

Every file has a single responsibility.

---

# Why This Design?

Suppose tomorrow you need to monitor Azure.

You only add:

```text
sensors/
└── azure.py
```

No changes are required to:

* exporter.py
* metrics.py
* HTTP server

The exporter automatically loads the new sensor from configuration.

This makes the system extensible.

---

# Design Principles

Throughout this repository, we'll follow these principles:

### Single Responsibility Principle

Each module should have one responsibility.

---

### Configuration Over Code

Behavior should come from YAML, not hard-coded values.

---

### Loose Coupling

Sensors should not depend on other sensors.

---

### Extensibility

Adding a new sensor should require minimal code changes.

---

### Least Privilege

Sensors should request only the permissions they need.

---

# Key Takeaways

* A good exporter is modular.
* Sensors collect data but do not expose metrics.
* The metrics layer translates observations into Prometheus metrics.
* Configuration determines what the exporter monitors.
* Monitoring scope (cluster or namespace) should come from configuration.
* A modular architecture makes it easy to add new sensors without changing the exporter core.

---

# Next Lesson

In the next lesson, we'll stop discussing architecture and begin implementing it.

We'll introduce **YAML configuration** and build a simple exporter that reads its behavior from a configuration file instead of hard-coded Python values.

This is the first step toward a production-ready, configurable exporter.





# 07. YAML Configuration

## Objective

By the end of this lesson, you will understand:

* Why configuration should be separated from code
* Why YAML is commonly used in cloud-native applications
* How our exporter will use configuration
* How to design a simple, extensible configuration file
* Configuration validation and best practices

---

# Why Not Hard-Code Everything?

Imagine your exporter contains this code:

```python
PORT = 8000

NAMESPACE = "monitoring"

SCRAPE_INTERVAL = 30
```

Now imagine another team wants:

* Port 9000
* Namespace `payments`
* Interval 60 seconds

You now have to edit Python code.

This doesn't scale.

Configuration should be external.

---

# Configuration vs Code

A good rule is:

**Code defines behavior.**

**Configuration defines values.**

For example:

Code:

```python
collect_metrics(namespace)
```

Configuration:

```yaml
namespace: monitoring
```

The logic never changes.

Only the configuration changes.

---

# Why YAML?

Cloud-native tools commonly use YAML.

Examples:

* Kubernetes
* Helm
* Argo CD
* GitHub Actions
* Prometheus
* Docker Compose
* Ansible

Since our exporter is designed for Kubernetes, YAML is the natural choice.

---

# What Should Be Configurable?

Our exporter should allow users to change operational settings without modifying Python.

Typical settings include:

* HTTP port
* Log level
* Monitoring scope
* Enabled sensors
* Sensor-specific settings

---

# Example Configuration

```yaml
exporter:
  port: 8000
  refresh_interval: 30

scope:
  mode: namespace
  namespace: monitoring

sensors:
  - type: kubernetes
    enabled: true
```

Everything that may differ between environments belongs here.

---

# Configuration Sections

## Exporter

Controls the exporter itself.

```yaml
exporter:
  port: 8000
  refresh_interval: 30
```

Possible future settings:

* Log level
* Bind address
* Metrics path
* Timeout

---

## Scope

Defines what the exporter can monitor.

```yaml
scope:
  mode: namespace
  namespace: monitoring
```

Supported modes:

```text
cluster

namespace

namespaces
```

Examples:

Cluster:

```yaml
scope:
  mode: cluster
```

Multiple namespaces:

```yaml
scope:
  mode: namespaces
  namespaces:
    - monitoring
    - security
```

---

## Sensors

Each sensor is configured independently.

```yaml
sensors:
  - type: kubernetes
    enabled: true
```

Later we might add:

```yaml
sensors:
  - type: kubernetes
    enabled: true

  - type: http
    enabled: true

  - type: wiz
    enabled: false
```

The exporter only loads enabled sensors.

---

# Sensor-Specific Configuration

Different sensors require different settings.

Example:

```yaml
sensors:
  - type: http
    enabled: true

    endpoints:
      - https://example.com/health
      - https://api.example.com/status
```

Another sensor:

```yaml
sensors:
  - type: kubernetes
    enabled: true

    include_namespaces:
      - monitoring
      - security
```

Each sensor owns its own configuration.

---

# Configuration Flow

```text
sensors.yaml
      │
      ▼
Configuration Loader
      │
      ▼
Validate
      │
      ▼
Create Configuration Object
      │
      ▼
Exporter
```

The rest of the exporter should never read the YAML file directly.

Only the configuration loader does that.

---

# Validation

Never assume the configuration is correct.

Example:

Incorrect:

```yaml
exporter:
  port: abc
```

The exporter should reject this configuration.

Another example:

```yaml
scope:
  mode: invalid
```

Again, fail early with a clear error.

---

# Defaults

Some values should have sensible defaults.

For example:

```yaml
exporter:
  port: 8000
```

If omitted:

```yaml
exporter: {}
```

the exporter could default to:

```text
Port = 8000
```

This reduces unnecessary configuration.

---

# Configuration Best Practices

Keep configuration:

* Human-readable
* Small
* Explicit
* Version-controlled

Avoid storing secrets such as:

* API tokens
* Passwords
* Client secrets

Instead, use:

* Environment variables
* Kubernetes Secrets
* External secret managers

Configuration should reference secrets, not contain them.

---

# Our Configuration Philosophy

The exporter should behave like this:

```text
Read Configuration
        │
        ▼
Initialize Components
        │
        ▼
Start Exporter
```

Changing behavior should require changing **YAML**, not **Python**.

---

# Initial Configuration for This Repository

We'll start with a very small configuration.

```yaml
exporter:
  port: 8000

scope:
  mode: namespace
  namespace: monitoring

sensors:
  - type: kubernetes
    enabled: true
```

As the repository evolves, we'll add more options without changing the overall structure.

---

# Looking Ahead

In the next coding lesson, we'll implement:

* A configuration loader using `PyYAML`
* Automatic validation
* Loading configuration into Python objects
* Passing configuration to the exporter

From that point onward, none of our code will rely on hard-coded values.

---

# Key Takeaways

* Configuration should be separated from application logic.
* YAML is the standard configuration format in the Kubernetes ecosystem.
* The exporter should be driven by configuration, not code changes.
* Validation prevents invalid configurations from causing runtime failures.
* Each sensor should own its own configuration block.
* Secrets should never be stored directly in configuration files.

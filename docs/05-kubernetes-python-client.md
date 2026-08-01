# 05. Kubernetes Python Client

## Objective

By the end of this lesson, you will understand:

* Why a Kubernetes client library exists
* How applications communicate with the Kubernetes API Server
* How the Python Kubernetes client works
* Authentication methods
* The basic objects you'll interact with
* The APIs we'll use in our exporter

---

# Why Do We Need a Kubernetes Client?

Everything in Kubernetes is managed through the Kubernetes API Server.

Whether you run:

```bash
kubectl get pods
```

or

```bash
kubectl get nodes
```

both commands ultimately communicate with the API Server.

```text
          kubectl
              |
              |
      HTTPS Request
              |
              v
+-------------------------+
| Kubernetes API Server   |
+-------------------------+
```

The Python client simply allows your Python program to do the same thing.

---

# kubectl vs Python Client

Consider this command:

```bash
kubectl get pods
```

Internally, Kubernetes performs something similar to:

```http
GET /api/v1/pods
```

Instead of using `kubectl`, Python calls the same API.

```python
v1.list_pod_for_all_namespaces()
```

Both return the same information.

The difference is:

* kubectl is for humans.
* Python is for applications.

---

# Kubernetes Architecture

```text
                +----------------------+
                |   API Server         |
                +----------+-----------+
                           ^
                           |
              HTTPS Requests
                           |
        +------------------+------------------+
        |                                     |
     kubectl                         Python Client
```

Every Kubernetes client talks to the API Server.

No component talks directly to Pods or Nodes.

---

# Installing the Client

Install using pip:

```bash
pip install kubernetes
```

or later through:

```text
requirements.txt
```

---

# Loading Configuration

The client must know **which cluster** to connect to.

There are two common methods.

## Local Development

```python
from kubernetes import config

config.load_kube_config()
```

This loads:

```text
~/.kube/config
```

which is the same configuration used by `kubectl`.

---

## Inside Kubernetes

When your application runs as a Pod:

```python
from kubernetes import config

config.load_incluster_config()
```

The cluster automatically provides credentials through the Pod's Service Account.

No kubeconfig file is required.

---

# Creating an API Client

After loading configuration:

```python
from kubernetes import client

v1 = client.CoreV1Api()
```

Think of this as opening a connection to the Kubernetes API.

Now you can query cluster resources.

---

# Listing Pods

```python
pods = v1.list_pod_for_all_namespaces()
```

The result contains every Pod.

Example:

```text
nginx-7bc7

grafana

prometheus

coredns
```

---

# Listing Nodes

```python
nodes = v1.list_node()
```

Example:

```text
worker-01

worker-02

control-plane
```

---

# Reading Namespaces

```python
namespaces = v1.list_namespace()
```

Example:

```text
default

kube-system

monitoring

production
```

---

# Object Model

The client does not return dictionaries.

It returns Python objects.

Example:

```python
for pod in pods.items:
    print(pod.metadata.name)
```

Output:

```text
grafana

prometheus

nginx
```

Here:

```text
pod
 ├── metadata
 │      └── name
 ├── spec
 └── status
```

Everything in Kubernetes follows a similar structure.

---

# Reading Pod Status

```python
for pod in pods.items:
    print(
        pod.metadata.name,
        pod.status.phase
    )
```

Example:

```text
grafana Running

prometheus Running

nginx Pending

job Failed
```

---

# Reading Node Status

```python
for node in nodes.items:
    print(node.metadata.name)
```

Later we'll inspect:

* Ready condition
* Capacity
* Allocatable resources

---

# Authentication

The Python client supports multiple authentication methods.

## Local kubeconfig

```text
~/.kube/config
```

Used during development.

---

## Service Account

Automatically mounted inside Pods.

Most production exporters use this.

---

## Token

Bearer token authentication.

Useful for automation.

---

## Client Certificates

Supported but less common.

---

# RBAC

The client can only access resources it has permission to read.

Example:

```text
Exporter
      |
      v
Service Account
      |
      v
Role / ClusterRole
      |
      v
API Server
```

Without proper RBAC, API calls fail with:

```text
403 Forbidden
```

---

# Error Handling

A cluster may be unreachable.

Always expect failures.

Example:

```python
try:
    pods = v1.list_pod_for_all_namespaces()
except Exception as ex:
    print(ex)
```

Production exporters should never crash because of a temporary API failure.

---

# How Our Exporter Will Use the Client

Our exporter won't monitor the entire cluster.

Instead, it will perform lightweight health checks.

Example:

```text
Exporter
      |
      v
Kubernetes API
      |
      v
Read Pod Status
      |
      v
Generate Metrics
```

For example:

```text
kubernetes_pods_running 27

kubernetes_nodes_ready 3

kubernetes_api_up 1
```

---

# API Flow

```text
Exporter
     |
     |
load_kube_config()
     |
Create CoreV1Api
     |
List Pods
     |
Read Status
     |
Generate Metrics
     |
Expose /metrics
     |
Prometheus Scrapes
```

This is exactly the pattern we'll implement in later lessons.

---

# APIs We'll Use

For this repository, we'll focus on a small set of APIs.

| API        | Purpose                      |
| ---------- | ---------------------------- |
| CoreV1Api  | Pods, Nodes, Namespaces      |
| AppsV1Api  | Deployments                  |
| BatchV1Api | Jobs and CronJobs (optional) |

These cover most exporter use cases.

---

# Key Takeaways

* Every Kubernetes operation goes through the API Server.
* The Python client is the programmatic equivalent of `kubectl`.
* Local development uses `load_kube_config()`.
* Applications running inside Kubernetes use `load_incluster_config()`.
* Resources are returned as Python objects.
* RBAC controls what your exporter can access.
* A production exporter should handle API failures gracefully.

---

# Looking Ahead

You've now completed the foundational theory required for this repository.

From the next lesson onward, we'll start designing the exporter you'll eventually use in the **Security Observability Platform**.

We'll introduce:

* A configurable project structure
* YAML-based sensor configuration
* Sensor abstraction
* Multiple sensor support
* Clean separation of configuration, collection, and metrics
* Extensible architecture that can support Kubernetes, HTTP APIs, Wiz, Prisma Cloud, and future integrations without changing the exporter core.






# Namespace vs Cluster Scope

One of the first architectural decisions when building a Kubernetes exporter is **what part of the cluster it should monitor**.

There are two common approaches:

* Cluster-scoped monitoring
* Namespace-scoped monitoring

Choosing the correct scope affects:

* Security
* RBAC permissions
* Deployment model
* Visibility

---

# Cluster-Scoped Monitoring

A cluster-scoped exporter can monitor resources across the entire Kubernetes cluster.

Example:

```text
                     Kubernetes Cluster
+------------------------------------------------------+
|                                                      |
| Namespace A      Namespace B      Namespace C         |
|                                                      |
|  Pods             Pods             Pods              |
|  Services         Services         Services          |
|                                                      |
+------------------------------------------------------+
                    ▲
                    │
            Cluster-wide Exporter
```

A cluster-scoped exporter typically reads:

* All Pods
* All Nodes
* All Namespaces
* All Deployments
* Cluster-wide resources

To do this, it requires:

* **ClusterRole**
* **ClusterRoleBinding**

Example API call:

```python
v1.list_pod_for_all_namespaces()
```

Advantages:

* Complete visibility
* Single exporter instance
* Suitable for platform or infrastructure teams

Limitations:

* Requires elevated permissions
* Not ideal for multi-tenant environments
* May expose information that application teams should not access

---

# Namespace-Scoped Monitoring

Many organizations do not allow applications to read the entire cluster.

Instead, each team owns one or more namespaces.

Example:

```text
Kubernetes Cluster

+-------------------+
| payments          |
|-------------------|
| Exporter          |
| Pods              |
| Services          |
+-------------------+

+-------------------+
| inventory         |
|-------------------|
| Pods              |
| Services          |
+-------------------+
```

In this model, the exporter only monitors resources within its assigned namespace.

Typical API call:

```python
v1.list_namespaced_pod(namespace)
```

Required permissions:

* **Role**
* **RoleBinding**

Advantages:

* Least-privilege access
* Better security
* Suitable for application teams
* Easier RBAC management

Limitations:

* Multiple exporter instances may be required
* Cannot monitor cluster-wide resources such as Nodes

---

# RBAC Comparison

| Cluster Scope             | Namespace Scope         |
| ------------------------- | ----------------------- |
| ClusterRole               | Role                    |
| ClusterRoleBinding        | RoleBinding             |
| Access to all namespaces  | Access to one namespace |
| Infrastructure monitoring | Application monitoring  |

Following the **Principle of Least Privilege**, namespace-scoped exporters should be preferred unless cluster-wide visibility is required.

---

# How Does an Exporter Know Which Namespace to Monitor?

There are several common approaches.

### Static Configuration

```yaml
scope:
  mode: namespace
  namespace: payments
```

---

### Multiple Namespaces

```yaml
scope:
  mode: namespaces
  namespaces:
    - payments
    - inventory
```

---

### Environment Variable

A deployment can provide the namespace through an environment variable.

```yaml
env:
- name: WATCH_NAMESPACE
  value: payments
```

Python:

```python
namespace = os.getenv("WATCH_NAMESPACE")
```

This pattern is widely used by Kubernetes Operators and Controllers.

---

### Automatically Detect Current Namespace

When running inside Kubernetes, every Pod receives its namespace through its Service Account.

The namespace is available at:

```text
/var/run/secrets/kubernetes.io/serviceaccount/namespace
```

Example:

```python
with open(
    "/var/run/secrets/kubernetes.io/serviceaccount/namespace"
) as f:
    namespace = f.read().strip()
```

This allows the exporter to automatically monitor the namespace in which it is deployed without requiring additional configuration.

---

# Which Approach Will We Use?

Our exporter will support both deployment models.

```text
                Configuration
                     │
             scope.mode
                     │
        +------------+------------+
        |                         |
     cluster                namespace
        |                         |
        +------------+------------+
                     │
            Kubernetes Sensor
                     │
              Generate Metrics
```

Example configuration:

```yaml
scope:
  mode: namespace
  namespace: monitoring
```

or

```yaml
scope:
  mode: cluster
```

The sensor implementation will remain the same. It simply receives the configured scope and queries the Kubernetes API accordingly.

This design makes the exporter flexible enough for both small application teams and platform-wide monitoring deployments.

---

# Design Principle

A well-designed exporter should **not assume cluster-wide access**.

Instead, it should:

* Support both cluster and namespace scopes
* Follow the Principle of Least Privilege
* Allow the monitoring scope to be configured rather than hard-coded
* Separate RBAC configuration from exporter logic

This makes the exporter secure, reusable, and suitable for production environments.

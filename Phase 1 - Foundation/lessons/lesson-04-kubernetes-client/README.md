# Lesson 04 - Kubernetes Python Client

## Objective

By the end of this lesson you will understand:

* Why Kubernetes exposes an API
* Why every Kubernetes operation goes through the API Server
* Why client libraries exist
* What the Kubernetes Python Client is
* How applications communicate with Kubernetes
* Why authentication and authorization are required
* Namespace-scoped vs Cluster-scoped access
* In-cluster vs Out-of-cluster applications

In this lesson we are **not** building an exporter yet.

First, we will understand the architecture.

---

# Looking Back

In Lesson 03 our exporter collected information from the operating system.

```text
Operating System
        │
        ▼
      psutil
        │
        ▼
 Read System Data
        │
        ▼
 Update Metrics
        │
        ▼
     /metrics
```

Notice something.

The Operating System never knew Prometheus existed.

Our exporter simply asked the operating system for information.

Now replace only one component.

```text
Kubernetes Cluster
        │
        ▼
 Kubernetes API Server
        │
        ▼
 Kubernetes Python Client
        │
        ▼
 Read Kubernetes Data
        │
        ▼
 Update Metrics
        │
        ▼
     /metrics
```

The architecture remains almost identical.

Only the data source changes.

---

# What Is Kubernetes?

Before we talk about Python, let's understand Kubernetes.

Many people think Kubernetes is:

* Pods
* Deployments
* Services
* Nodes

Those are Kubernetes **resources**.

Kubernetes itself is a platform that manages those resources.

Think of Kubernetes as a distributed operating system for containers.

Just like Linux manages:

* Processes
* Memory
* CPU
* Files

Kubernetes manages:

* Pods
* Deployments
* Services
* ConfigMaps
* Secrets
* Nodes
* Namespaces
* Jobs
* Persistent Volumes

---

# Can Python Directly Read Pods?

Imagine writing this:

```python
pods = read_all_pods()
```

Question:

Where would Python get this information?

Python has no built-in knowledge of Kubernetes.

Unlike the operating system, Kubernetes runs as another distributed system.

Python needs someone to answer questions such as:

* What Pods exist?
* What Deployments exist?
* What Namespace does this Pod belong to?
* Is this Pod healthy?

Who answers those questions?

---

# The Kubernetes API Server

The answer is:

**The Kubernetes API Server**

The API Server is the front door of Kubernetes.

Every request goes through it.

Examples:

```text
kubectl get pods
```

↓

API Server

---

```text
kubectl create deployment
```

↓

API Server

---

```text
kubectl delete pod
```

↓

API Server

---

```text
Python Client
```

↓

API Server

---

Even Kubernetes components communicate through the API Server.

There is no shortcut.

---

# Why Does Everything Go Through the API Server?

Imagine allowing every application to directly modify cluster state.

One application changes Pods.

Another modifies Secrets.

Another edits Deployments.

Soon the cluster becomes inconsistent.

Instead Kubernetes has one rule.

Everything goes through one entry point.

That entry point is the API Server.

The API Server is responsible for:

* Authentication
* Authorization
* Validation
* Admission Controllers
* Updating cluster state

It is the central control plane component.

---

# A Real Example

Suppose you execute:

```bash
kubectl get pods
```

Most beginners think:

```text
kubectl

↓

Pod List
```

That is not what happens.

The real flow is:

```text
kubectl

↓

API Server

↓

etcd

↓

API Server

↓

kubectl
```

The API Server reads the cluster state and returns the response.

Exactly the same thing happens with Python.

```text
Python

↓

Kubernetes Python Client

↓

API Server

↓

Response
```

The client never talks directly to Pods.

---

# What Is the Kubernetes Python Client?

The Kubernetes Python Client is simply a Python library.

Its responsibility is:

* Build Kubernetes API requests
* Authenticate
* Send requests
* Parse responses

It is equivalent to:

* psutil for Linux
* boto3 for AWS
* azure-identity + Azure SDK for Azure
* requests for generic HTTP APIs

It is **not** Kubernetes.

It is only a client.

---

# Why Not Use requests?

Technically, you can.

For example:

```python
requests.get(
    "https://cluster-api/api/v1/pods"
)
```

But then you must manually handle:

* Authentication
* TLS Certificates
* API Paths
* JSON Parsing
* Kubernetes Object Models
* Version Compatibility

The Python Client already solves these problems.

That is why almost every Python application uses it.

---

# The Mental Model

Never think:

```text
Python

↓

Pods
```

Instead think:

```text
Python

↓

Kubernetes Python Client

↓

API Server

↓

Cluster Resources
```

This is the architecture used by:

* Operators
* Controllers
* Exporters
* Admission Controllers
* Custom Automation
* Platform Engineering Tools

---

# Knowledge Check

Before continuing, answer these questions.

1. Does Python communicate directly with Pods?
2. What is the single entry point into a Kubernetes cluster?
3. Why does Kubernetes require all requests to pass through the API Server?
4. Is the Kubernetes Python Client part of Kubernetes?
5. Could you use the `requests` library instead of the Kubernetes Python Client?

Do not continue until you can confidently answer these questions.

---

# Next Part

In Part 2 we will learn:

* kubeconfig
* Authentication
* Service Accounts
* In-cluster vs Out-of-cluster
* RBAC
* Namespace-scoped vs Cluster-scoped permissions

These concepts determine **what your exporter is allowed to monitor**.
-------
# Lesson 04 - Kubernetes Python Client (Part 2)

## Authentication and Authorization

Before Python can read anything from Kubernetes, two questions must be answered.

```
Who are you?

What are you allowed to do?
```

These are two completely different questions.

Kubernetes answers them separately.

---

# Authentication

Authentication answers:

> **Who are you?**

Examples:

* Human user
* Administrator
* Developer
* CI/CD Pipeline
* Prometheus Exporter
* Argo CD
* GitHub Actions

If Kubernetes cannot identify you, the request is rejected immediately.

Authentication happens before authorization.

---

# Authorization

After Kubernetes knows **who you are**, it asks another question.

> **What are you allowed to do?**

For example:

```
Developer

↓

Can read Pods

✓ Yes

↓

Can delete Nodes

✗ No
```

Authentication identifies you.

Authorization determines your permissions.

---

# Example

Suppose your exporter sends:

```
List all Pods
```

Kubernetes asks:

```
Who is requesting?
```

Exporter answers:

```
Service Account
```

Kubernetes now checks:

```
Is this Service Account allowed to list Pods?
```

If yes:

```
Return Pods
```

If not:

```
403 Forbidden
```

---

# kubeconfig

When you run:

```bash
kubectl get pods
```

How does `kubectl` know:

* Which cluster?
* Which user?
* Which certificates?

The answer is:

```
kubeconfig
```

Usually located at:

```text
~/.kube/config
```

This file contains:

* Cluster information
* User credentials
* Context
* Certificates

It tells client applications how to connect to Kubernetes.

---

# Out-of-Cluster Applications

Suppose you run Python on your laptop.

```
Laptop

↓

Python

↓

Kubernetes Cluster
```

How does Python authenticate?

Using:

```
kubeconfig
```

This is called:

> **Out-of-Cluster Configuration**

Because the application is running outside Kubernetes.

---

# In-Cluster Applications

Now imagine your exporter runs inside Kubernetes.

```
Exporter Pod

↓

API Server
```

There is no kubeconfig.

Instead Kubernetes automatically provides:

* Service Account Token
* Cluster Certificate
* API Server Address

The exporter simply uses those credentials.

This is called:

> **In-Cluster Configuration**

---

# Service Accounts

Earlier we asked:

> Who are you?

For applications, the answer is usually:

```
Service Account
```

A Service Account represents an application running inside Kubernetes.

Examples:

* Prometheus
* Argo CD
* Metrics Server
* Your Exporter

Each application should have its own Service Account.

---

# Why Not Use the Admin Account?

Imagine giving every application full administrator access.

Now suppose one exporter is compromised.

The attacker could:

* Delete Pods
* Read Secrets
* Modify Deployments
* Delete Namespaces

This violates the Principle of Least Privilege.

Instead:

Every application receives only the permissions it actually needs.

---

# RBAC

RBAC stands for:

```
Role-Based Access Control
```

RBAC determines:

* Who can read
* Who can create
* Who can update
* Who can delete

Kubernetes enforces these permissions through:

* Roles
* ClusterRoles
* RoleBindings
* ClusterRoleBindings

We'll learn each of these later.

For now, remember:

RBAC controls access.

---

# Namespace-Scoped Permissions

Suppose your cluster contains:

```
default

monitoring

production

development
```

Your exporter only needs to monitor:

```
monitoring
```

Should it receive access to the entire cluster?

No.

Instead we grant permission only inside:

```
monitoring
```

Now the exporter cannot read Pods in:

```
production
```

This improves security.

---

# Cluster-Scoped Permissions

Some exporters need information about the entire cluster.

Examples:

* Nodes
* All Namespaces
* Cluster Events

These require cluster-wide permissions.

Such exporters typically use:

```
ClusterRole

+

ClusterRoleBinding
```

because Roles are limited to a single namespace.

---

# Which One Will We Build?

Our exporter should support both.

Example:

```
clusterScope: true
```

Monitor the entire cluster.

or

```
clusterScope: false

namespace: monitoring
```

Monitor only one namespace.

This is exactly why we designed the exporter to be configuration-driven.

The monitoring scope should change through configuration—not code.

---

# Architecture

Out-of-Cluster

```
Laptop

↓

Python

↓

kubeconfig

↓

API Server

↓

Pods
```

---

In-Cluster

```
Exporter Pod

↓

Service Account

↓

API Server

↓

Pods
```

Notice something.

Only the authentication method changes.

Everything else remains identical.

---

# Why This Matters for Our Exporter

Later we will support:

```
Single Namespace

Multiple Namespaces

Entire Cluster
```

The exporter code should remain the same.

Only:

* Service Account
* RBAC
* Configuration

should determine what the exporter can see.

This is one of the core design goals of our Security Observability Platform.

---

# Knowledge Check

Answer these questions before moving to Part 3.

1. What is the difference between Authentication and Authorization?
2. What is kubeconfig?
3. When is kubeconfig used?
4. What is a Service Account?
5. Why shouldn't applications use the cluster-admin account?
6. What is RBAC?
7. What is the difference between a Role and a ClusterRole?
8. When should an exporter use namespace-scoped permissions?
9. When should an exporter use cluster-scoped permissions?
10. If your exporter only monitors one namespace, what permissions should it receive?

---

# Next Part

In Part 3 we will finally start writing code.

We'll learn:

* Installing the Kubernetes Python Client
* Connecting to a cluster
* Reading Pods
* Reading Namespaces
* Reading Nodes
* Building the first Kubernetes exporter

-------
# Lesson 04 - Kubernetes Python Client (Part 3)

## Objective

By the end of this part you will:

* Install the Kubernetes Python Client
* Connect to a Kubernetes cluster
* Read Namespaces
* Read Pods
* Read Nodes
* Understand how Kubernetes objects are returned
* Build the foundation for the first Kubernetes exporter

---

# Hands-on Task 1 - Install the Client

Install the Kubernetes Python Client.

```bash
pip install kubernetes
```

Update the project dependencies.

```bash
pip freeze > requirements.txt
```

Verify the installation.

```bash
pip show kubernetes
```

Observe:

* Version
* Installation path

---

# Hands-on Task 2 - Prediction

Before writing any code, answer this question.

Earlier we used:

```python
import psutil
```

Now we will use:

```python
from kubernetes import client, config
```

Question:

What do you think these two modules are responsible for?

Predict before continuing.

---

# Theory

The Kubernetes Python Client is divided into multiple modules.

The two most common are:

```python
config
```

and

```python
client
```

Think of them as having different responsibilities.

```text
config
     │
     ▼
Establish Connection

client
     │
     ▼
Talk to Kubernetes APIs
```

Never mix these responsibilities.

---

# Hands-on Task 3 - Connect to Kubernetes

Create:

```text
lesson-04-kubernetes-client/connect.py
```

Add:

```python
from kubernetes import client, config

config.load_kube_config()

print("Connected Successfully")
```

Run:

```bash
python connect.py
```

---

## Prediction

Before running the program, answer:

What do you think:

```python
config.load_kube_config()
```

actually does?

Choose your own explanation before executing the code.

---

# Theory

Remember:

Your Python application does not know:

* Which cluster exists
* Where the API Server is
* Which user to authenticate as
* Which certificates to use

`load_kube_config()` reads the kubeconfig file and configures the client accordingly.

Conceptually:

```text
Python

↓

load_kube_config()

↓

Read ~/.kube/config

↓

Cluster Information

↓

Authentication

↓

Ready to call API Server
```

Notice:

No request has been sent yet.

The client is only preparing the connection.

---

# Hands-on Task 4 - Read Namespaces

Replace the code with:

```python
from kubernetes import client, config

config.load_kube_config()

v1 = client.CoreV1Api()

namespaces = v1.list_namespace()

for namespace in namespaces.items:
    print(namespace.metadata.name)
```

Run it.

Observe:

* How many namespaces exist?
* What is returned by `list_namespace()`?

---

# Prediction

Before running the code, answer:

What do you think:

```python
namespaces
```

contains?

Choose one.

A)

```text
A list of strings
```

B)

```text
A JSON document
```

C)

```text
A Kubernetes API object containing Namespace objects
```

D)

```text
A dictionary
```

---

# Theory

The Kubernetes Client does not return plain text.

It returns Python objects representing Kubernetes resources.

For example:

```python
namespace.metadata.name
```

means:

```text
Namespace Object

↓

Metadata

↓

Name
```

This is similar to what we learned with:

```python
memory.percent
```

from `psutil`.

Both libraries return objects instead of raw strings.

---

# Hands-on Task 5 - Read Pods

Replace the previous code.

```python
from kubernetes import client, config

config.load_kube_config()

v1 = client.CoreV1Api()

pods = v1.list_pod_for_all_namespaces()

for pod in pods.items:
    print(
        pod.metadata.namespace,
        pod.metadata.name
    )
```

Observe:

* Namespace
* Pod Name

---

# Prediction

Suppose the cluster contains:

```text
frontend

backend

database
```

Question:

Do you think:

```python
pod.metadata.name
```

returns:

```text
frontend
```

or

```text
Pod Object
```

Predict before running.

---

# Hands-on Task 6 - Read Nodes

Now replace the code again.

```python
from kubernetes import client, config

config.load_kube_config()

v1 = client.CoreV1Api()

nodes = v1.list_node()

for node in nodes.items:
    print(node.metadata.name)
```

Observe:

* Number of Nodes
* Node Names

---

# Architecture Review

Notice the pattern.

Read Namespaces

```text
Python

↓

CoreV1Api()

↓

API Server

↓

Namespace Objects
```

Read Pods

```text
Python

↓

CoreV1Api()

↓

API Server

↓

Pod Objects
```

Read Nodes

```text
Python

↓

CoreV1Api()

↓

API Server

↓

Node Objects
```

Only the API method changes.

Everything else remains identical.

---

# Looking Ahead

In the next lesson we will stop printing Kubernetes objects.

Instead we will convert them into Prometheus metrics.

Example:

```text
kubernetes_pod_status

kubernetes_namespace_count

kubernetes_node_ready
```

The exporter architecture will remain exactly the same.

The only difference is that instead of printing the values, we will expose them through `/metrics`.

---

# Knowledge Check

Before moving to Lesson 05, answer these questions.

1. What is the responsibility of `config`?
2. What is the responsibility of `client`?
3. Does `load_kube_config()` contact the API Server?
4. What does `CoreV1Api()` represent?
5. Why does the client return Kubernetes objects instead of strings?
6. What information is available inside `metadata`?
7. Which API method lists Namespaces?
8. Which API method lists Pods?
9. Which API method lists Nodes?
10. What changes between reading Pods and reading Nodes?

---

# Key Takeaways

* `config` prepares the client to connect to Kubernetes.
* `client` sends requests to the Kubernetes API Server.
* Kubernetes resources are returned as Python objects.
* Different API methods retrieve different resource types.
* The overall exporter architecture remains the same regardless of the resource being collected.
* The next step is converting Kubernetes objects into Prometheus metrics.

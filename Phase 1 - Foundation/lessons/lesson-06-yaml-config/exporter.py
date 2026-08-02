from kubernetes import client, config
from prometheus_client import Gauge, start_http_server
import time
import yaml
config.load_kube_config()
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
running_pods = Gauge(
    "kubernetes_running_pods",
    "Total number of running pods"
)

v1 = client.CoreV1Api()
start_http_server(config["server"]["port"])
while True:
    pods = v1.list_pod_for_all_namespaces()
    running_pod=0
    for pod in pods.items:
        if pod.status.phase == "Running":
            running_pod=running_pod+1
    running_pods.set(running_pod)
    time.sleep(config["exporter"]["poll_interval"])
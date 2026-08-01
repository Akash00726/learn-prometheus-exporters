from prometheus_client import Gauge, start_http_server
import time
import psutil

system_cpu_usage_percent = Gauge(
    "cpu_usage",
    "How much CPU utilized"
)

system_memory_usage_percent = Gauge(
    "memory_usage",
    "How much memory utilized"
)

system_disk_usage_percent = Gauge(
    "disk_usage",
    "How much disk utilized"
)
start_http_server(8000)
while True:
    cpu = psutil.cpu_percent(interval=1)
    system_cpu_usage_percent.set(cpu)
    memory = psutil.virtual_memory()
    system_memory_usage_percent.set(memory.percent)
    disk = psutil.disk_usage("/")
    system_disk_usage_percent.set(disk.percent)
    time.sleep(1)
    

from prometheus_client import Counter, start_http_server
import time

requests = Counter(
    "akash_requests_total",
    "Total requests served"
)

start_http_server(8000)

while True:
    requests.dec()

    print("Request Count Increased")

    time.sleep(2)
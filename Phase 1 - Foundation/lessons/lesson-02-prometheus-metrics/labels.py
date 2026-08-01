from prometheus_client import Gauge, start_http_server
import time

temperature = Gauge(
    "room_temperature",
    "Room Temperature",
    ["room"]
)

start_http_server(8000)

temperature.labels(room="bedroom").set(25)

temperature.labels(room="kitchen").set(28)

temperature.labels(room="office").set(24)

while True:
    time.sleep(1)
from prometheus_client import Gauge, start_http_server
import time
t_value = 20
h_value = 60
temperature = Gauge(
    "temperature",
    "Room Temperature"
)

humidity = Gauge(
    "humid",
    "Room Humidity"
)

start_http_server(8000)

print("Exporter Started")



while True:
    t_value = t_value+1
    h_value = h_value+1
    temperature.set(t_value)
    humidity.set(h_value)
    time.sleep(1)
    if t_value>30:
        t_value = 20
    if h_value>70:
        h_value = 60
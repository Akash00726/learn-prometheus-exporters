import psutil
import time

while True:
    cpu = psutil.cpu_percent(interval=1)

    print(cpu)

    time.sleep(5)
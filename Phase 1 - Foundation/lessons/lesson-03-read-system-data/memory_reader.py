import psutil
import time

while True:
    memory = psutil.virtual_memory()

    print(memory)

    time.sleep(5)
import serial
import time
import json
import random

ser = serial.Serial("COM3", 115200)

while True:
    msg = {
        "src": "ADC1",
        "ch": 0,
        "name": "servo_1",
        "unit": "A",
        "val": round(random.uniform(0.5, 2.0), 2),
        "ts": time.time()
    }

    ser.write((json.dumps(msg) + "\n").encode())
    time.sleep(0.1)

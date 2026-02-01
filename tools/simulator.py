import socket
import json
import time
import random

HOST = "127.0.0.1"
PORT = 9000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

channels = [
    ("ADC1", 0, "servo_1", "A"),
    ("ADC1", 1, "servo_2", "A"),
    ("ADC2", 0, "bus_voltage", "V"),
    ("THERM", 0, "motor_temp", "C"),
]

print("Simulator connected → sending data")

while True:
    src, ch, name, unit = random.choice(channels)

    value = {
        "A": random.uniform(0.2, 2.5),
        "V": random.uniform(10, 12.6),
        "C": random.uniform(25, 70),
    }[unit]

    msg = {
        "ts": time.time(),
        "src": src,
        "ch": ch,
        "name": name,
        "unit": unit,
        "val": round(value, 3),
    }

    line = json.dumps(msg) + "\n"
    sock.sendall(line.encode())

    time.sleep(0.05)  # 20Hz

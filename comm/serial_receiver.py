import serial
import time


def start_serial_receiver(port, baudrate=115200):
    """
    Generator:
    يقرأ سطر JSON من USB ويرجعه للـ engine
    """
    while True:
        try:
            print(f"[USB] Trying to open {port} ...")
            ser = serial.Serial(port, baudrate, timeout=1)
            print("[USB] Connected")

            buffer = ""

            while True:
                data = ser.read().decode(errors="ignore")
                if not data:
                    continue

                if data == "\n":
                    line = buffer.strip()
                    buffer = ""
                    if line:
                        yield line
                else:
                    buffer += data

        except serial.SerialException as e:
            print("[USB] Disconnected, retrying...", e)
            time.sleep(2)

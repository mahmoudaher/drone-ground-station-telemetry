import threading
from queue import Queue

from comm.tcp_receiver import start_tcp_server
from comm.ws_server import start_ws_server, broadcast_ws
from core.parser import parse_line
from core.buffers import add_sample
from storage.csv_logger import log_row
from comm.serial_receiver import start_serial_receiver


queue = Queue(maxsize=10000)


def receiver_worker():
    print("Receiver thread started")
    for line in start_tcp_server():
        queue.put(line)


def processor_worker():
    print("Processor thread started")
    while True:
        line = queue.get()
        data = parse_line(line)

        if data:
            add_sample(data)
            broadcast_ws(data)
            log_row(data)

        queue.task_done()




def usb_receiver_worker():
    for line in start_serial_receiver(port="COM3", baudrate=115200):
        queue.put(line)



def start_engine():
    print("Engine starting...")

    t_wifi = threading.Thread(target=receiver_worker, daemon=True)
    t_usb = threading.Thread(target=usb_receiver_worker, daemon=True)
    t_proc = threading.Thread(target=processor_worker, daemon=True)
    t_ws = threading.Thread(target=start_ws_server, daemon=True)

    t_wifi.start()
    t_usb.start()
    t_proc.start()
    t_ws.start()

    t_wifi.join()

import threading
from queue import Queue

from comm.tcp_receiver import start_tcp_server
from core.parser import parse_line
from storage.csv_logger import log_row
from core.buffers import add_sample
from comm.ui_broadcaster import start_ui_server, broadcast



queue = Queue(maxsize=10000)


# Receiver Thread
def receiver_worker():
    print("Receiver thread started")

    for line in start_tcp_server():
        queue.put(line)



# Processor Thread
def processor_worker():
    print("Processor thread started")

    while True:
        line = queue.get()

        data = parse_line(line)

        if data:
             add_sample(data)
             broadcast(data)
             log_row(data)

        queue.task_done()




# Engine start
def start_engine():
    t1 = threading.Thread(target=receiver_worker, daemon=True)
    t2 = threading.Thread(target=processor_worker, daemon=True)
    t3 = threading.Thread(target=start_ui_server, daemon=True)

    t1.start()
    t2.start()
    t3.start()

    t1.join()

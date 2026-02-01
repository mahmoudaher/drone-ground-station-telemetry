import socket

def start_tcp_server(host="0.0.0.0", port=9000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)

    print(f"TCP server listening on {port} ...")
    conn, addr = server.accept()
    print("Client connected:", addr)

    buffer = ""

    while True:
        data = conn.recv(4096).decode()
        if not data:
            break

        buffer += data

        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            yield line

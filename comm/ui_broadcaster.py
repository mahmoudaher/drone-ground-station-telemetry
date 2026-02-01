import socket
import json

clients = []


def start_ui_server(host="127.0.0.1", port=9100):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"UI broadcaster listening on {port}")

    while True:
        conn, addr = server.accept()
        print("UI connected:", addr)
        clients.append(conn)


def broadcast(data: dict):
    msg = json.dumps(data) + "\n"
    dead = []

    for c in clients:
        try:
            c.sendall(msg.encode())
        except:
            dead.append(c)

    for d in dead:
        clients.remove(d)

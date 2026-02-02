import asyncio
import json
import websockets

clients = set()


async def ws_handler(websocket):
    print("[WS] UI connected")
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)
        print("[WS] UI disconnected")


async def ws_server(host="127.0.0.1", port=9200):
    print(f"[WS] Server listening on {port}")
    async with websockets.serve(ws_handler, host, port):
        await asyncio.Future()  # run forever


def start_ws_server():
    asyncio.run(ws_server())


def broadcast_ws(data: dict):
    if not clients:
        return

    msg = json.dumps(data)

    async def _broadcast():
        dead = []
        for ws in clients:
            try:
                await ws.send(msg)
            except:
                dead.append(ws)
        for d in dead:
            clients.remove(d)

    asyncio.run(_broadcast())

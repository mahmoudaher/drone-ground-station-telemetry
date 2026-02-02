import asyncio
import json
import websockets
import threading

clients = set()
loop = None


async def handler(ws):
    print("UI connected")
    clients.add(ws)
    try:
        await ws.wait_closed()
    finally:
        clients.remove(ws)
        print("UI disconnected")


async def broadcast(data: dict):
    if not clients:
        return

    msg = json.dumps(data)
    for ws in clients:
        try:
            await ws.send(msg)
        except:
            pass


def start_websocket_server(host="0.0.0.0", port=8765):
    global loop
    
    async def main():
        async with websockets.serve(handler, host, port):
            print(f"WebSocket server running on {port}")
            await asyncio.Future()  # run forever

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())


def broadcast_from_thread(data: dict):
    """Thread-safe broadcast function to be called from non-async context"""
    global loop
    if loop is not None:
        asyncio.run_coroutine_threadsafe(broadcast(data), loop)

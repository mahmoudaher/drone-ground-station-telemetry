import time
import socket
import json
import threading
import streamlit as st
from core.buffers import add_sample
from core.buffers import list_channels, get_buffer

def ui_listener(host="127.0.0.1", port=9100):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    buffer = ""

    while True:
        data = sock.recv(4096).decode()
        buffer += data

        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            d = json.loads(line)
            add_sample(d)


st.set_page_config(page_title="Drone Telemetry", layout="wide")
if "listener_started" not in st.session_state:
    t = threading.Thread(target=ui_listener, daemon=True)
    t.start()
    st.session_state.listener_started = True


st.title("🚁 Drone Ground Station")

placeholder = st.empty()

while True:
    with placeholder.container():
        st.subheader("Live Channels")

        channels = list_channels()

        if not channels:
            st.warning("No data yet...")
        else:
            for ch in channels:
                st.markdown(f"### Channel: {ch}")

                data = get_buffer(ch)

                if data:
                    times, values = zip(*data)
                    st.line_chart(values)
                else:
                    st.text("No samples yet")

    time.sleep(0.5)

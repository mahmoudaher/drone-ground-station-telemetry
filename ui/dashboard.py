import time
import json
import threading
import asyncio
import streamlit as st
import websockets

from core.buffers import add_sample, list_channels, get_buffer
from config.channels import CHANNEL_NAMES
from config.thresholds import THRESHOLDS

# widgets
from ui.widgets.health_panel import render_health_panel
from ui.widgets.stats_panel import render_stats_panel
from ui.widgets.control_panel import channel_toggle
from ui.widgets.gauges import render_gauge
from ui.widgets.graph_styles import render_colored_graph


# ======================================================
# WebSocket Listener (Engine -> UI)
# ======================================================

def ws_listener():
    async def _listen():
        uri = "ws://127.0.0.1:9200"
        while True:
            try:
                async with websockets.connect(uri) as ws:
                    print("[UI] WebSocket connected")
                    async for msg in ws:
                        try:
                            d = json.loads(msg)
                            add_sample(d)
                        except json.JSONDecodeError:
                            pass
            except Exception as e:
                print("[UI] WS error, retrying...", e)
                await asyncio.sleep(1)

    asyncio.run(_listen())


# ======================================================
# Streamlit setup
# ======================================================

st.set_page_config(
    page_title="Drone Telemetry",
    layout="wide"
)

# شغّل WebSocket listener مرة واحدة فقط
if "listener_started" not in st.session_state:
    t = threading.Thread(target=ws_listener, daemon=True)
    t.start()
    st.session_state.listener_started = True


# ======================================================
# Header + Top Status Bar (UX)
# ======================================================

st.title("🚁 Drone Ground Station")

st.markdown(
    """
    <style>
    .top-bar {
        display: flex;
        justify-content: space-between;
        padding: 10px 15px;
        background-color: #0e1117;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .badge {
        padding: 6px 12px;
        border-radius: 8px;
        font-weight: bold;
        background-color: #262730;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="top-bar">
        <div class="badge">🟢 Connection: Active</div>
        <div class="badge">📡 Channels: {len(list_channels())}</div>
        <div class="badge">⏱ Refresh: 500 ms</div>
    </div>
    """,
    unsafe_allow_html=True
)


# ======================================================
# Sidebar – Global Controls
# ======================================================

st.sidebar.header("⚙️ Global Control")
pause = st.sidebar.toggle("⏸️ Pause Graphs", value=False)


# ======================================================
# Helpers
# ======================================================

def channel_group(ch):
    if ch.startswith("ADC1"):
        return "Motors"
    if ch.startswith("ADC2"):
        return "Power"
    if ch.startswith("THERM"):
        return "Thermal"
    return "Other"


def get_thresholds(name):
    t = THRESHOLDS.get(name, {})
    return (
        t.get("warn", float("inf")),
        t.get("danger", float("inf")),
    )


# ======================================================
# Collect & Group Data (for health panel)
# ======================================================

channels = list_channels()

grouped_values = {
    "Motors": [],
    "Power": [],
    "Thermal": []
}

for ch in channels:
    name = CHANNEL_NAMES.get(ch, ch)
    data = get_buffer(ch)
    group = channel_group(ch)

    if data and group in grouped_values:
        _, values = zip(*data)
        grouped_values[group].extend(values)


# ======================================================
# Health Summary Panel
# ======================================================

render_health_panel(grouped_values)

st.divider()


# ======================================================
# Main Tabs with Grid Layout
# ======================================================

tabs = st.tabs(["Motors", "Power", "Thermal"])

for tab_name, tab in zip(["Motors", "Power", "Thermal"], tabs):
    with tab:
        tab_channels = [ch for ch in channels if channel_group(ch) == tab_name]

        if not tab_channels:
            st.info("⏳ Waiting for telemetry...")
            continue

        cols = st.columns(2)

        for i, ch in enumerate(tab_channels):
            with cols[i % 2]:
                name = CHANNEL_NAMES.get(ch, ch)
                data = get_buffer(ch)

                # Enable / Disable channel
                enabled = channel_toggle(name)
                if not enabled:
                    continue

                if not data:
                    st.info("⏳ Waiting for data...")
                    continue

                _, values = zip(*data)
                last_value = values[-1]

                warn, danger = get_thresholds(name)

                # Gauge
                render_gauge(
                    name=name,
                    value=last_value,
                    unit="",
                    warn=warn,
                    danger=danger
                )

                # Stats
                render_stats_panel(name, values)

                # Graph
                if pause:
                    st.info("Graphs paused")
                else:
                    render_colored_graph(
                        values=values,
                        warn=warn,
                        danger=danger
                    )

                st.divider()


# ======================================================
# Auto refresh
# ======================================================

time.sleep(0.5)
st.rerun()

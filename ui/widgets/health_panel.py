import streamlit as st

def render_health_panel(channels_data):
    st.subheader("🩺 System Health")

    cols = st.columns(4)

    def status_color(ok):
        return "🟢 OK" if ok else "🔴 ISSUE"

    battery_ok = all(v < 13 for v in channels_data.get("Power", []))
    motors_ok = all(v < 2.5 for v in channels_data.get("Motors", []))
    temp_ok = all(v < 70 for v in channels_data.get("Thermal", []))

    cols[0].metric("Battery", status_color(battery_ok))
    cols[1].metric("Motors", status_color(motors_ok))
    cols[2].metric("Temperature", status_color(temp_ok))
    cols[3].metric("Connection", "🟢 Active")

import streamlit as st

def render_gauge(name, value, unit, warn, danger):
    if value >= danger:
        color = "🔴"
    elif value >= warn:
        color = "🟡"
    else:
        color = "🟢"

    st.metric(
        label=f"{name}",
        value=f"{value:.2f} {unit}",
        delta=color
    )

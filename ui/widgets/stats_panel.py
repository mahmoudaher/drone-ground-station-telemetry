import streamlit as st
import numpy as np

def render_stats_panel(name, values):
    st.caption("Statistics")

    if not values:
        st.text("No data")
        return

    col1, col2, col3 = st.columns(3)

    col1.metric("Min", f"{np.min(values):.2f}")
    col2.metric("Max", f"{np.max(values):.2f}")
    col3.metric("Avg", f"{np.mean(values):.2f}")

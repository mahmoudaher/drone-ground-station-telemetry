import streamlit as st
import pandas as pd

def render_colored_graph(values, warn, danger):
    df = pd.DataFrame({"value": values})

    st.line_chart(df)

    st.caption(
        f"🟢 < {warn} | 🟡 {warn}–{danger} | 🔴 > {danger}"
    )

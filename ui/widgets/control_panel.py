import streamlit as st

def channel_toggle(channel_name):
    return st.checkbox(f"Enable {channel_name}", value=True)

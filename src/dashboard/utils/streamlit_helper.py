import streamlit as st


def reset_slider(change_key, change_value):
    st.session_state[change_key] = change_value

import streamlit as st
import os

def selected_theme():
    st.set_page_config(
        page_title="Worklense HR BI",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Find style.css in current or .streamlit directory
    css_paths = ["style.css", ".streamlit/style.css"]
    css_found = False
    for css_path in css_paths:
        if os.path.exists(css_path):
            with open(css_path) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            css_found = True
            break
    if not css_found:
        st.warning("Custom style.css not found. App will use default Streamlit styles.")

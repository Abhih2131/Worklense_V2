import streamlit as st
import plotly.io as pio

def selected_theme():
    st.set_page_config(
        page_title="Worklense HR BI",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    plotly_themes = {
        "Default": "plotly",
        "White Classic": "plotly_white",
        "GGPlot Style": "ggplot2",
        "Seaborn Style": "seaborn",
        "Simple White": "simple_white",
        "Presentation": "presentation",
        "Grid On": "gridon",
        "No Theme (None)": "none"
    }
    plotly_theme_label = st.sidebar.selectbox(
        "Chart Style (Plotly Theme)",
        options=list(plotly_themes.keys()),
        index=0
    )
    st.session_state["plotly_template"] = plotly_themes[plotly_theme_label]

    st.markdown(
        """
        <style>
        body, .main, .stApp {
            font-family: 'Segoe UI', 'Inter', Arial, sans-serif !important;
            background: #f6f8fa !important;
            color: #22223b !important;
        }
        section[data-testid="stSidebar"] {
            background: #142A4F !important;
            color: white !important;
        }
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] label {
            color: white !important;
            font-weight: 500;
        }
        section[data-testid="stSidebar"] .stSelectbox,
        section[data-testid="stSidebar"] .stMultiSelect {
            background: #142A4F !important;
        }
        section[data-testid="stSidebar"] .stMultiSelect span[aria-label][data-baseweb="tag"] {
            background: #406080 !important;
            color: white !important;
            border: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

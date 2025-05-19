import streamlit as st
import plotly.io as pio

def selected_theme():
    # Set Streamlit page config for title and layout
    st.set_page_config(
        page_title="Worklense HR BI",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # --- APP THEME SELECTOR ---
    themes = {
        "Light": "#f7f9fb",
        "Classic Blue": "#eef4ff",
        "Dark": "#1a2234"
    }
    selected = st.sidebar.selectbox("Theme Selector", list(themes.keys()))
    bg_color = themes[selected]
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {bg_color}; }}
        </style>
    """, unsafe_allow_html=True)

    # --- PLOTLY CHART STYLE SELECTOR (Dynamic) ---
    plotly_theme_names = list(pio.templates)
    plotly_theme_label = st.sidebar.selectbox(
        "Chart Style (Plotly Theme)",
        options=plotly_theme_names,
        index=0
    )
    st.session_state["plotly_template"] = plotly_theme_label

    # Inject global CSS for custom fonts and sidebar styling (your existing CSS)
    st.markdown(
        """
        <style>
        /* Global font and background */
        body, .main, .stApp {
            font-family: 'Segoe UI', 'Inter', Arial, sans-serif !important;
            background: #f6f8fa !important;
            color: #22223b !important;
        }
        /* Sidebar styling */
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

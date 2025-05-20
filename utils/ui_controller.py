import streamlit as st
import plotly.io as pio
from utils.data_handler import filter_dataframe, ensure_datetime

def setup_sidebar(emp_df):
    # Branding in sidebar
    st.sidebar.markdown("<h2 style='color:#fff;'>Worklense Reports</h2>", unsafe_allow_html=True)

    # --- Chart Style selector at bottom of sidebar ---
    main_themes = {
        "Default": "plotly",
        "White Classic": "plotly_white",
        "Seaborn": "seaborn",
        "Presentation": "presentation"
    }
    st.sidebar.markdown("---")
    plotly_theme_label = st.sidebar.selectbox(
        "Chart Style (Plotly Theme)",
        options=list(main_themes.keys()),
        index=0
    )
    st.session_state["plotly_template"] = main_themes[plotly_theme_label]

    # --- Filters ---
    filter_columns = [
        "company", "business_unit", "department", "function",
        "zone", "area", "band", "employment_type"
    ]
    filter_dict = {}

    with st.sidebar.expander("Show Filters", expanded=False):
        n_cols = 2
        for row_start in range(0, len(filter_columns), n_cols):
            cols = st.sidebar.columns(n_cols)
            for i in range(n_cols):
                col_idx = row_start + i
                if col_idx >= len(filter_columns):
                    continue
                col = filter_columns[col_idx]
                options = sorted([str(x) for x in emp_df[col].dropna().unique()])
                key = f"sidebar_{col}"
                with cols[i]:
                    chosen = st.multiselect(
                        col.replace("_", " ").title(),
                        options=options,
                        default=[],
                        key=key
                    )
                    filter_dict[col] = options if not chosen else chosen

    # Apply filters
    filtered_emp = filter_dataframe(emp_df, filter_dict)
    filtered_emp = ensure_datetime(filtered_emp, ['date_of_joining', 'date_of_exit', 'date_of_birth'])
    return filtered_emp, filter_dict

def render_branding():
    st.markdown("""
    <div class='custom-header'>
      <div class='header-left'>
        <div class='brand-name'>Worklense</div>
        <div class='brand-tagline'>A Smarter Lens for Better Decisions</div>
      </div>
      <div class='header-right'>
        <a href="https://yourhelp.site" target="_blank">Help</a>
      </div>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown(
        "<div class='custom-footer'>© 2025 Worklense HR Analytics | All rights reserved.</div>",
        unsafe_allow_html=True
    )

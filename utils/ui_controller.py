import streamlit as st
import os

def setup_sidebar(emp_df):
    # 1. Report selector at top
    report_folder = "reports"
    report_modules = [f[:-3] for f in os.listdir(report_folder) if f.endswith(".py") and not f.startswith("_")]
    selected_report = st.sidebar.selectbox(
        "Select Report",
        report_modules,
        format_func=lambda x: x.replace("_", " ").title()
    )
    st.session_state["selected_report"] = selected_report

    # 2. Multi-select filters (in single container, minimal spacing)
    company = st.sidebar.multiselect("Company", sorted(emp_df['company'].dropna().unique()))
    business_unit = st.sidebar.multiselect("Business Unit", sorted(emp_df['business_unit'].dropna().unique()))
    department = st.sidebar.multiselect("Department", sorted(emp_df['department'].dropna().unique()))
    function = st.sidebar.multiselect("Function", sorted(emp_df['function'].dropna().unique()))
    zone = st.sidebar.multiselect("Zone", sorted(emp_df['zone'].dropna().unique()))
    area = st.sidebar.multiselect("Area", sorted(emp_df['area'].dropna().unique()))
    band = st.sidebar.multiselect("Band", sorted(emp_df['band'].dropna().unique()))
    employment_type = st.sidebar.multiselect("Employment Type", sorted(emp_df['employment_type'].dropna().unique()))

    filter_dict = {
        "company": company,
        "business_unit": business_unit,
        "department": department,
        "function": function,
        "zone": zone,
        "area": area,
        "band": band,
        "employment_type": employment_type,
    }

    # 3. Chart style selector at bottom, with minimal spacing above
    st.sidebar.markdown('<div style="margin-top: 10px"></div>', unsafe_allow_html=True)
    chart_styles = ["Default", "White Classic", "Seaborn", "Plotly", "Dark"]
    chart_style = st.sidebar.selectbox("Chart Style (Plotly Theme)", chart_styles)

    # 4. Apply filters to the dataframe (data updates as filters change)
    filtered_df = emp_df.copy()
    for col, selected in filter_dict.items():
        if selected:
            filtered_df = filtered_df[filtered_df[col].isin(selected)]

    return filtered_df, filter_dict

def render_footer():
    st.markdown("""
        <div class="custom-footer">
            © 2025 Worklense HR Analytics | All rights reserved.
        </div>
    """, unsafe_allow_html=True)

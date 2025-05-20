import streamlit as st
from utils.data_handler import load_all_data
from utils.chart_renderer import (
    render_line_chart, render_bar_chart,
    render_pie_chart, render_donut_chart
)
from reports.executive_summary import run_report
from kpi_design import render_kpi_card

# --- Load Data ---
data_files = {
    'employee_master': 'data/employee_master.xlsx',
    'leave': 'data/HRMS_Leave.xlsx',
    'sales': 'data/Sales_INR.xlsx'
}
data = load_all_data(data_files)
config = {}

# --- Run Executive Summary Report (returns KPIs & DataFrames) ---
report = run_report(data, config)

# --- UI: Executive Summary ---
st.title("Executive Summary")

# --- KPIs ---
for i in range(0, len(report["kpis"]), 4):
    cols = st.columns(4)
    for j in range(4):
        idx = i + j
        if idx >= len(report["kpis"]): break
        kpi = report["kpis"][idx]
        with cols[j]:
            st.markdown(render_kpi_card(kpi['label'], kpi['value'], kpi['type']), unsafe_allow_html=True)

# --- Charts (2 per row) ---
charts = [
    ("Manpower Growth", render_line_chart, report["manpower_growth"], {"x": "FY", "y": "Headcount"}),
    ("Manpower Cost Trend", render_bar_chart, report["manpower_cost"], {"x": "FY", "y": "Total Cost"}),
    ("Attrition Trend", render_line_chart, report["attrition"], {"x": "FY", "y": "Attrition %"}),
    ("Gender Diversity", render_donut_chart, report["gender"], {"names": "Gender", "values": "Count"}),
    ("Age Distribution", render_pie_chart, report["age"], {"names": "Age Group", "values": "Count"}),
    ("Tenure Distribution", render_pie_chart, report["tenure"], {"names": "Tenure Group", "values": "Count"}),
    ("Total Experience Distribution", render_bar_chart, report["experience"], {"x": "Experience Group", "y": "Count"}),
    ("Education Type Distribution", render_donut_chart, report["education"], {"names": "Qualification", "values": "Count"}),
]

for i in range(0, len(charts), 2):
    cols = st.columns(2, gap="large")
    for j in range(2):
        idx = i + j
        if idx >= len(charts): break
        title, render_func, df_chart, params = charts[idx]
        with cols[j]:
            st.markdown(f"##### {title}")
            render_func(df_chart, **params)

# --- Footer (Optional) ---
st.markdown(
    "<div class='custom-footer'>© 2025 Worklense HR Analytics | All rights reserved.</div>",
    unsafe_allow_html=True
)

import streamlit as st
import os
import importlib
from utils.data_handler import load_all_data, ensure_datetime, filter_dataframe
from utils.chart_renderer import *
from kpi_design import render_kpi_card
from theme_handler import selected_theme

selected_theme()

# --- Data Loading ---
data_files = {
    'employee_master': 'data/employee_master.xlsx',
    'leave': 'data/HRMS_Leave.xlsx',
    'sales': 'data/Sales_INR.xlsx'
}
data = load_all_data(data_files)
config = {}

# --- Sidebar: Auto-discover reports ---
def get_report_modules():
    report_folder = "reports"
    files = [f for f in os.listdir(report_folder) if f.endswith(".py") and not f.startswith("_")]
    modules = [f[:-3] for f in files]
    return modules

report_modules = get_report_modules()
selected_report = st.sidebar.selectbox(
    "Select Report",
    report_modules,
    format_func=lambda x: x.replace("_", " ").title()
)

# --- Filters (copy your previous logic here) ---
# (You can keep the filters code from before, so all reports get the same filters.)

# --- Filter Data ---
emp_df = data['employee_master']
# ... (filter logic as before) ...
# Apply filters to employee_master as needed
data['employee_master'] = emp_df  # (after filter applied)

# --- Dynamically import and run selected report ---
if selected_report:
    mod = importlib.import_module(f"reports.{selected_report}")
    if hasattr(mod, "run_report"):
        report = mod.run_report(data, config)
        # Render KPIs and charts as before, but reading keys from the report dict
        st.title(selected_report.replace("_", " ").title())
        # KPIs (if present)
        if "kpis" in report:
            for i in range(0, len(report["kpis"]), 4):
                cols = st.columns(4)
                for j in range(4):
                    idx = i + j
                    if idx >= len(report["kpis"]): break
                    kpi = report["kpis"][idx]
                    with cols[j]:
                        st.markdown(render_kpi_card(kpi['label'], kpi['value'], kpi['type']), unsafe_allow_html=True)
        # Charts (if present)
        chart_keys = [k for k in report if k not in ("kpis", "fy_list", "as_of")]
        for i in range(0, len(chart_keys), 2):
            cols = st.columns(2, gap="large")
            for j in range(2):
                idx = i + j
                if idx >= len(chart_keys): break
                chart_key = chart_keys[idx]
                chart_df = report[chart_key]
                # Use a convention or config in the report for chart type:
                # For now, just example (improve per report)
                with cols[j]:
                    st.markdown(f"##### {chart_key.replace('_', ' ').title()}")
                    # Example: guess chart function by key
                    if "cost" in chart_key:
                        render_bar_chart(chart_df, x="FY", y="Total Cost")
                    elif "attrition" in chart_key:
                        render_line_chart(chart_df, x="FY", y="Attrition %")
                    elif "growth" in chart_key:
                        render_line_chart(chart_df, x="FY", y="Headcount")
                    elif "gender" in chart_key or "donut" in chart_key:
                        render_donut_chart(chart_df, names="Gender", values="Count")
                    elif "age" in chart_key or "tenure" in chart_key:
                        render_pie_chart(chart_df, names=chart_df.columns[0], values=chart_df.columns[1])
                    elif "experience" in chart_key:
                        render_bar_chart(chart_df, x="Experience Group", y="Count")
                    elif "education" in chart_key:
                        render_donut_chart(chart_df, names="Qualification", values="Count")
                    else:
                        st.dataframe(chart_df)
    else:
        st.error(f"Report module '{selected_report}' must have a 'run_report(data, config)' function.")

# --- Footer ---
st.markdown(
    "<div class='custom-footer'>© 2025 Worklense HR Analytics | All rights reserved.</div>",
    unsafe_allow_html=True
)

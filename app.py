import streamlit as st
import os
import importlib
from utils.data_handler import load_all_data
from utils.ui_controller import setup_sidebar, render_branding, render_footer
from kpi_design import render_kpi_card
from utils.chart_renderer import *

# --- Data loading ---
data_files = {
    'employee_master': 'data/employee_master.xlsx',
    'leave': 'data/HRMS_Leave.xlsx',
    'sales': 'data/Sales_INR.xlsx'
}
data = load_all_data(data_files)
emp_df = data['employee_master']

# --- UI: Branding, Sidebar/Filters, Theme selection ---
filtered_emp, filter_dict = setup_sidebar(emp_df)
data['employee_master'] = filtered_emp
render_branding()

# --- Reports: Dynamic discovery from 'reports' folder ---
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

# --- Run & render selected report ---
if selected_report:
    mod = importlib.import_module(f"reports.{selected_report}")
    if hasattr(mod, "run_report"):
        report = mod.run_report(data, {})
        st.title(selected_report.replace("_", " ").title())
        if "kpis" in report:
            for i in range(0, len(report["kpis"]), 4):
                cols = st.columns(4)
                for j in range(4):
                    idx = i + j
                    if idx >= len(report["kpis"]): break
                    kpi = report["kpis"][idx]
                    with cols[j]:
                        st.markdown(render_kpi_card(kpi['label'], kpi['value'], kpi['type']), unsafe_allow_html=True)
        # --- Charts: 2 per row, basic heuristics ---
        chart_keys = [k for k in report if k not in ("kpis", "fy_list", "as_of")]
        for i in range(0, len(chart_keys), 2):
            cols = st.columns(2, gap="large")
            for j in range(2):
                idx = i + j
                if idx >= len(chart_keys): break
                chart_key = chart_keys[idx]
                chart_df = report[chart_key]
                with cols[j]:
                    st.markdown(f"##### {chart_key.replace('_', ' ').title()}")
                    # Basic auto-chart logic (can customize further per report)
                    if "cost" in chart_key:
                        render_bar_chart(chart_df, x="FY", y="Total Cost")
                    elif "attrition" in chart_key:
                        render_line_chart(chart_df, x="FY", y="Attrition %")
                    elif "growth" in chart_key:
                        render_line_chart(chart_df, x="FY", y="Headcount")
                    elif "gender" in chart_key:
                        render_donut_chart(chart_df, names="Gender", values="Count")
                    elif "age" in chart_key:
                        render_pie_chart(chart_df, names="Age Group", values="Count")
                    elif "tenure" in chart_key:
                        render_pie_chart(chart_df, names="Tenure Group", values="Count")
                    elif "experience" in chart_key:
                        render_bar_chart(chart_df, x="Experience Group", y="Count")
                    elif "education" in chart_key:
                        render_donut_chart(chart_df, names="Qualification", values="Count")
                    else:
                        st.dataframe(chart_df)
    else:
        st.error(f"Report module '{selected_report}' must have a 'run_report(data, config)' function.")

render_footer()

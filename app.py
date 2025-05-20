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

# --- Sidebar: Filters + Chart Theme + Branding (this must be BEFORE report is run!) ---
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
        # (KPI/charts rendering logic here)
    else:
        st.error(f"Report module '{selected_report}' must have a 'run_report(data, config)' function.")

render_footer()

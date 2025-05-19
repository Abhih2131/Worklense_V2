# app.py
import streamlit as st
import os
import importlib
from utils.data_handler import load_all_data, load_config

# --- PAGE CONFIG ---
st.set_page_config(page_title="HR BI App", layout="wide")

# --- LOAD DATA & CONFIG ---
data_files = {
    'employee_master': 'data/employee_master.xlsx',
    'leave': 'data/HRMS_Leave.xlsx',
    'sales': 'data/Sales_INR.xlsx'
}
config_file = 'config/report_config.xlsx'

# Data: dict of DataFrames
data = load_all_data(data_files)
# Config: dict of DataFrames (one per sheet)
config = load_config(config_file)

# --- DISCOVER REPORTS ---
def get_report_modules():
    report_folder = "reports"
    files = [f for f in os.listdir(report_folder) if f.endswith(".py") and not f.startswith("__")]
    modules = [f[:-3] for f in files]
    return modules

report_modules = get_report_modules()

# --- SIDEBAR: Report Selector ---
st.sidebar.title("HR BI Reports")
selected_report = st.sidebar.selectbox(
    "Select Report",
    report_modules,
    format_func=lambda x: x.replace("_", " ").title()
)

# --- MAIN AREA: Load Selected Report Module Dynamically ---
if selected_report:
    mod = importlib.import_module(f"reports.{selected_report}")
    if hasattr(mod, "run_report"):
        mod.run_report(data, config)
    else:
        st.error(f"Report module '{selected_report}' must have a 'run_report(data, config)' function.")

# --- UAT & RUN CHECKLIST ---
# 1. Code modular and imports only what’s needed.
# 2. Reports loaded dynamically from /reports folder.
# 3. Data and config loaded once, shared with all reports.
# 4. Fails gracefully if report file doesn’t have run_report.
# 5. Ready for extension—just add new .py files in /reports.

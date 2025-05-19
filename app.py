# app.py

import streamlit as st
import os
import importlib
from utils.data_handler import load_all_data, ensure_datetime, filter_dataframe

st.set_page_config(page_title="HR BI App", layout="wide")

# --- Data load ---
data_files = {
    'employee_master': 'data/employee_master.xlsx',
    'leave': 'data/HRMS_Leave.xlsx',
    'sales': 'data/Sales_INR.xlsx'
}
data = load_all_data(data_files)
config = {}

# --- Modular report loading ---
def get_report_modules():
    report_folder = "reports"
    files = [f for f in os.listdir(report_folder) if f.endswith(".py") and not f.startswith("__")]
    modules = [f[:-3] for f in files]
    return modules

report_modules = get_report_modules()

# --- Sidebar: Reports first, then filters below ---
st.sidebar.title("HR BI Reports")
selected_report = st.sidebar.selectbox(
    "Select Report",
    report_modules,
    format_func=lambda x: x.replace("_", " ").title()
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")

filter_columns = ["company", "business_unit", "department", "function", "zone", "area", "band", "employment_type"]
emp_df = data['employee_master']
filter_dict = {}
for col in filter_columns:
    options = sorted([str(x) for x in emp_df[col].dropna().unique()])
    # By default, select all options
    selected = st.sidebar.multiselect(
        col.replace("_", " ").title(),
        options=options,
        default=options,
        key=f"sidebar_{col}"
    )
    filter_dict[col] = selected

# --- Apply filter to all reports globally ---
filtered_emp = filter_dataframe(emp_df, filter_dict)
filtered_emp = ensure_datetime(filtered_emp, ['date_of_joining', 'date_of_exit', 'date_of_birth'])
data['employee_master'] = filtered_emp

# --- Run the selected report ---
if selected_report:
    mod = importlib.import_module(f"reports.{selected_report}")
    if hasattr(mod, "run_report"):
        mod.run_report(data, config)
    else:
        st.error(f"Report module '{selected_report}' must have a 'run_report(data, config)' function.")

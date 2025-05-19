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

# --- Sidebar Filter Summary (Side-by-Side Display, Not Selectable) ---
st.sidebar.title("Filters")
filter_columns = ["company", "business_unit", "department", "function", "zone", "area", "band", "employment_type"]

with st.sidebar:
    st.markdown("#### Filter Status")
    cols = st.columns(len(filter_columns))
    for i, col in enumerate(filter_columns):
        with cols[i]:
            st.markdown(
                f"""
                <div style='
                    background:#e7f2fb;
                    border-radius:10px;
                    padding:6px 8px;
                    margin-bottom:4px;
                    text-align:center;
                    font-size:0.92rem;
                    color:#19577a;
                '>
                <b>{col.replace('_', ' ').title()}</b><br>
                <span style='font-size:1rem; color:#057fa6;'>All</span>
                </div>
                """, unsafe_allow_html=True
            )

# --- Prepare filtered data for reports (all "All", so not filtered) ---
emp_df = data['employee_master']
filter_dict = {col: [] for col in filter_columns}
filtered_emp = filter_dataframe(emp_df, filter_dict)
filtered_emp = ensure_datetime(filtered_emp, ['date_of_joining', 'date_of_exit', 'date_of_birth'])
data['employee_master'] = filtered_emp

# --- Modular report loading ---
def get_report_modules():
    report_folder = "reports"
    files = [f for f in os.listdir(report_folder) if f.endswith(".py") and not f.startswith("__")]
    modules = [f[:-3] for f in files]
    return modules

report_modules = get_report_modules()
st.sidebar.title("HR BI Reports")
selected_report = st.sidebar.selectbox(
    "Select Report",
    report_modules,
    format_func=lambda x: x.replace("_", " ").title()
)

if selected_report:
    mod = importlib.import_module(f"reports.{selected_report}")
    if hasattr(mod, "run_report"):
        mod.run_report(data, config)
    else:
        st.error(f"Report module '{selected_report}' must have a 'run_report(data, config)' function.")

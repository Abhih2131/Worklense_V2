# app.py

import streamlit as st
import os
import importlib
from utils.data_handler import load_all_data, ensure_datetime, filter_dataframe

st.set_page_config(page_title="Worklense", layout="wide")

# === Inject global CSS ===
try:
    with open("config/style.css") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Custom CSS file not found.")

# === Header (Worklense brand) ===
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

# --- Sidebar: Report select at top, then filter expander ---
st.sidebar.title("Worklense Reports")
selected_report = st.sidebar.selectbox(
    "Select Report",
    report_modules,
    format_func=lambda x: x.replace("_", " ").title()
)

st.sidebar.markdown("**Filters**")

filter_columns = [
    "company", "business_unit", "department", "function",
    "zone", "area", "band", "employment_type"
]
emp_df = data['employee_master']
filter_dict = {}

with st.sidebar.expander("Show Filters", expanded=False):
    n_cols = 2  # Two filters per row
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
                # If nothing selected, treat as "All" for filter logic
                if not chosen:
                    filter_dict[col] = options
                else:
                    filter_dict[col] = chosen

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

# === Footer (Worklense brand) ===
st.markdown(
    "<div class='custom-footer'>© 2025 Worklense HR Analytics | All rights reserved.</div>",
    unsafe_allow_html=True
)

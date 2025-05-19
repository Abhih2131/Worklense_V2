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

# --- Sidebar: Report select at top, then filter expander ---
st.sidebar.title("HR BI Reports")
selected_report = st.sidebar.selectbox(
    "Select Report",
    report_modules,
    format_func=lambda x: x.replace("_", " ").title()
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")

filter_columns = [
    "company", "business_unit", "department", "function",
    "zone", "area", "band", "employment_type"
]
emp_df = data['employee_master']
filter_dict = {}

with st.sidebar.expander("Show Filters", expanded=False):
    n_cols = 2  # Two filters per row
    for row_start in range(0, len(filter_columns), n_cols):
        cols = st.columns(n_cols)
        for i in range(n_cols):
            col_idx = row_start + i
            if col_idx >= len(filter_columns):
                continue
            col = filter_columns[col_idx]
            options = sorted([str(x) for x in emp_df[col].dropna().unique()])
            key = f"sidebar_{col}"

            # --- Custom: Only show pills if not all selected, else show "All" label ---
            selected = st.session_state.get(key, options)
            with cols[i]:
                st.write(f"**{col.replace('_', ' ').title()}**")
                if set(selected) == set(options):
                    st.text_input(" ", value="All", key=f"all_{col}", disabled=True, label_visibility="collapsed")
                    filter_dict[col] = options
                else:
                    chosen = st.multiselect(
                        "",
                        options=options,
                        default=selected,
                        key=key,
                        label_visibility="collapsed"
                    )
                    filter_dict[col] = chosen
                    st.session_state[key] = chosen

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

import streamlit as st
import importlib
import os

from theme_handler import selected_theme
from kpi_design import render_kpi_card
from utils.data_handler import load_all_data
from utils.ui_controller import setup_sidebar, render_footer

selected_theme()

data_files = {
    'employee_master': 'data/employee_master.xlsx',
    'leave': 'data/HRMS_Leave.xlsx',
    'sales': 'data/Sales_INR.xlsx'
}
data = load_all_data(data_files)
emp_df = data['employee_master']

filtered_emp, filter_dict = setup_sidebar(emp_df)
data['employee_master'] = filtered_emp

st.markdown("""
    <div class="custom-header">
        <span class="brand-name">Worklense</span>
        <span class="brand-tagline">A Smarter Lens for Better Decisions</span>
    </div>
    """, unsafe_allow_html=True)

report_folder = "reports"
report_modules = [f[:-3] for f in os.listdir(report_folder) if f.endswith(".py") and not f.startswith("_")]
selected_report = st.session_state.get("selected_report")
if not selected_report:
    selected_report = report_modules[0]
    st.session_state["selected_report"] = selected_report

if selected_report:
    mod = importlib.import_module(f"reports.{selected_report}")
    if hasattr(mod, "run_report"):
        report = mod.run_report(data, {})
        st.title(selected_report.replace("_", " ").title())

        # KPIs: 4 per row, wrap to next row
        kpis = report.get("kpis", [])
        for i in range(0, len(kpis), 4):
            cols = st.columns(4)
            for j, kpi in enumerate(kpis[i:i+4]):
                with cols[j]:
                    st.markdown(render_kpi_card(kpi["label"], kpi["value"], kpi.get("type", "Integer")), unsafe_allow_html=True)

        # Charts: 2 per row, wrap to next row
        charts = report.get("charts", [])
        for i in range(0, len(charts), 2):
            cols = st.columns(2)
            for j, chart in enumerate(charts[i:i+2]):
                with cols[j]:
                    st.plotly_chart(chart, use_container_width=True)
    else:
        st.error(f"Report module '{selected_report}' must have a 'run_report(data, config)' function.")

render_footer()

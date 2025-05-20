import streamlit as st
import importlib
import os

from theme_handler import selected_theme
from kpi_design import render_kpi_card
from utils.data_handler import load_all_data
from utils.ui_controller import setup_sidebar, render_footer

# 1. Apply global theme and CSS first
selected_theme()

# 2. Load all data
data_files = {
    'employee_master': 'data/employee_master.xlsx',
    'leave': 'data/HRMS_Leave.xlsx',
    'sales': 'data/Sales_INR.xlsx'
}
data = load_all_data(data_files)
emp_df = data['employee_master']

# 3. Setup sidebar (filters at top, chart style at bottom)
filtered_emp, filter_dict = setup_sidebar(emp_df)
data['employee_master'] = filtered_emp

# 4. Render header branding at top of main content
st.markdown("""
    <div class="custom-header">
        <span class="brand-name">Worklense</span>
        <span class="brand-tagline">A Smarter Lens for Better Decisions</span>
    </div>
    """, unsafe_allow_html=True)

# 5. Dynamic report selection (auto-list .py files from reports folder)
report_folder = "reports"
report_modules = [f[:-3] for f in os.listdir(report_folder) if f.endswith(".py") and not f.startswith("_")]
selected_report = st.sidebar.selectbox(
    "Select Report",
    report_modules,
    format_func=lambda x: x.replace("_", " ").title()
)

# 6. Run & render selected report (show KPIs + charts)
if selected_report:
    mod = importlib.import_module(f"reports.{selected_report}")
    if hasattr(mod, "run_report"):
        report = mod.run_report(data, {})
        st.title(selected_report.replace("_", " ").title())

        # Render KPI cards
        kpis = report.get("kpis", [])
        if kpis:
            kpi_cols = st.columns(len(kpis))
            for i, kpi in enumerate(kpis):
                with kpi_cols[i]:
                    st.markdown(render_kpi_card(kpi["label"], kpi["value"], kpi.get("type", "Integer")), unsafe_allow_html=True)

        # Render charts (assume each chart in report returns plotly or matplotlib fig)
        charts = report.get("charts", [])
        for chart in charts:
            st.plotly_chart(chart, use_container_width=True)

    else:
        st.error(f"Report module '{selected_report}' must have a 'run_report(data, config)' function.")

# 7. Footer
render_footer()

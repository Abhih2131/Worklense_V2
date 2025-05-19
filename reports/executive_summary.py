# reports/executive_summary.py

import streamlit as st
import pandas as pd
from datetime import datetime
from kpi_design import render_kpi_card

def run_report(data, config):
    st.title("Executive Summary")

    filtered_df = data.get("employee_master", pd.DataFrame())

    today = pd.Timestamp.now().normalize()
    fy_start = pd.Timestamp('2025-04-01')
    fy_end = pd.Timestamp('2026-03-31')

    # ... [KPI calculations as before] ...

    kpis = [
        {"label": "Active Employees", "value": active, "type": "Integer"},
        {"label": "Attrition Rate (FY 25-26)", "value": attrition, "type": "Percentage"},
        {"label": "Joiners (FY 25-26)", "value": joiners, "type": "Integer"},
        {"label": "Total Cost (INR)", "value": total_cost, "type": "Currency"},
        {"label": "Female Ratio", "value": female_ratio, "type": "Percentage"},
        {"label": "Avg Tenure", "value": avg_tenure, "type": "Years"},
        {"label": "Avg Age", "value": avg_age, "type": "Years"},
        {"label": "Avg Total Exp", "value": avg_total_exp, "type": "Years"},
    ]

    # 4 cards per row, pass idx for color
    for i in range(0, len(kpis), 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            if idx >= len(kpis):
                break
            kpi = kpis[idx]
            with cols[j]:
                st.markdown(
                    render_kpi_card(kpi['label'], kpi['value'], kpi['type'], idx),
                    unsafe_allow_html=True
                )

    st.subheader("Charts")
    st.info("Charts will appear here in future releases.")
    st.button("Export KPIs to Excel (Coming Soon)")

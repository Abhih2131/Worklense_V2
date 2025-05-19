# reports/executive_summary.py

import streamlit as st
import pandas as pd

def run_report(data, config):
    st.title("Executive Summary")

    # --- Load KPIs and Chart Config ---
    kpi_config = config.get("ExecutiveSummary_KPIs", pd.DataFrame())
    chart_config = config.get("ExecutiveSummary_Charts", pd.DataFrame())

    # --- Filters (Demo Only, Can Extend) ---
    st.write("Filters will go here.")

    # --- KPIs ---
    st.subheader("Key Metrics (KPIs)")
    if not kpi_config.empty:
        cols = st.columns(len(kpi_config))
        for idx, row in kpi_config.iterrows():
            with cols[idx]:
                st.metric(label=row["Display_Label"], value="--")  # Placeholder, will compute real values
    else:
        st.info("No KPI config found for Executive Summary.")

    # --- Charts ---
    st.subheader("Charts")
    if not chart_config.empty:
        for idx, row in chart_config.iterrows():
            st.write(f"**{row['Chart_Title']}**")
            st.write("Chart will go here.")  # Placeholder for charts
    else:
        st.info("No Chart config found for Executive Summary.")

    # --- Export to Excel Placeholder ---
    st.button("Export KPIs to Excel (Coming Soon)")

# UAT Checklist:
# - File imports with no errors
# - Function is called via app.py
# - Shows KPIs and chart placeholders per config
# - Handles missing config gracefully

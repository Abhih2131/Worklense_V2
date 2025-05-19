import streamlit as st
import pandas as pd

FILTER_COLS = [
    "company", "business_unit", "department", "function",
    "zone", "area", "band", "employment_type"
]

def run_report(data, config):
    st.title("Executive Summary")

    emp_df = data.get("employee_master", pd.DataFrame())

    # --- FILTER UI ---
    st.markdown("### Filters")
    filtered_df = emp_df.copy()
    filter_values = {}

    if not emp_df.empty:
        cols = st.columns(len(FILTER_COLS))
        for idx, col in enumerate(FILTER_COLS):
            unique_vals = ["All"] + sorted([str(x) for x in emp_df[col].dropna().unique()])
            selected = cols[idx].selectbox(col.replace("_", " ").title(), unique_vals)
            filter_values[col] = selected
            if selected != "All":
                filtered_df = filtered_df[filtered_df[col] == selected]
    else:
        st.warning("Employee Master data not found.")

    # --- KPIs ---
    st.subheader("Key Metrics (KPIs)")
    kpi_config = config.get("ExecutiveSummary_KPIs", pd.DataFrame())
    if not kpi_config.empty:
        cols = st.columns(len(kpi_config))
        for idx, row in kpi_config.iterrows():
            with cols[idx]:
                st.metric(label=row["Display_Label"], value="--")  # Placeholder for now
    else:
        st.info("No KPI config found for Executive Summary.")

    # --- Charts ---
    st.subheader("Charts")
    chart_config = config.get("ExecutiveSummary_Charts", pd.DataFrame())
    if not chart_config.empty:
        for idx, row in chart_config.iterrows():
            st.write(f"**{row['Chart_Title']}**")
            st.write("Chart will go here.")  # Placeholder for charts
    else:
        st.info("No Chart config found for Executive Summary.")

    st.button("Export KPIs to Excel (Coming Soon)")

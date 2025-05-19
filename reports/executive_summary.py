import streamlit as st
import pandas as pd
from datetime import datetime

FILTER_COLS = [
    "company", "business_unit", "department", "function",
    "zone", "area", "band", "employment_type"
]

def run_report(data, config):
    st.title("Executive Summary")

    emp_df = data.get("employee_master", pd.DataFrame())
    filtered_df = emp_df.copy()

    # --- FILTER UI (Hidden by default, show on button click) ---
    show_filters = st.button("Show Filters")
    filter_values = {}

    if show_filters and not emp_df.empty:
        with st.expander("Filters", expanded=True):
            cols = st.columns(len(FILTER_COLS))
            for idx, col in enumerate(FILTER_COLS):
                unique_vals = ["All"] + sorted([str(x) for x in emp_df[col].dropna().unique()])
                selected = cols[idx].selectbox(col.replace("_", " ").title(), unique_vals)
                filter_values[col] = selected
                if selected != "All":
                    filtered_df = filtered_df[filtered_df[col] == selected]

    # --- KPI Calculations ---
    headcount = len(filtered_df)
    active_employees = (filtered_df['employment_status'] == 'Active').sum()
    total_cost = filtered_df['total_ctc_pa'].sum()
    # Avoid division by zero
    attrition_rate = (
        (filtered_df['employment_status'] == 'Inactive').sum() / headcount * 100
        if headcount > 0 else 0
    )
    female_ratio = (
        (filtered_df['gender'] == 'Female').sum() / headcount * 100
        if headcount > 0 else 0
    )
    # Joiners in current year
    this_year = datetime.now().year
    joiners = filtered_df['date_of_joining'].apply(
        lambda x: pd.to_datetime(x).year if pd.notnull(x) else None
    ).eq(this_year).sum() if 'date_of_joining' in filtered_df else 0
    # Average Tenure (in years)
    avg_tenure = filtered_df['total_exp_yrs'].mean() if 'total_exp_yrs' in filtered_df else 0
    # Average Age (approx, from date_of_birth)
    def calc_age(dob):
        if pd.isnull(dob): return None
        return (datetime.now() - pd.to_datetime(dob)).days // 365
    avg_age = filtered_df['date_of_birth'].apply(calc_age).mean() if 'date_of_birth' in filtered_df else 0

    # --- Display KPIs (4 per row) ---
    kpi_labels = [
        "Headcount", "Active", "Attrition (%)", "Total Cost (INR)",
        "Female (%)", "Joiners", "Avg Tenure (yrs)", "Avg Age"
    ]
    kpi_values = [
        f"{headcount:,}",
        f"{active_employees:,}",
        f"{attrition_rate:.1f}%",
        f"₹{total_cost:,.0f}",
        f"{female_ratio:.1f}%",
        f"{joiners:,}",
        f"{avg_tenure:.1f}",
        f"{avg_age:.1f}"
    ]
    for i in range(0, 8, 4):
        cols = st.columns(4)
        for j in range(4):
            with cols[j]:
                st.metric(label=kpi_labels[i+j], value=kpi_values[i+j])

    # --- Charts Placeholder ---
    st.subheader("Charts")
    chart_config = config.get("ExecutiveSummary_Charts", pd.DataFrame())
    if not chart_config.empty:
        for idx, row in chart_config.iterrows():
            st.write(f"**{row['Chart_Title']}**")
            st.write("Chart will go here.")
    else:
        st.info("No Chart config found for Executive Summary.")

    st.button("Export KPIs to Excel (Coming Soon)")

# UAT Checklist:
# - 8 KPIs in 2 rows (4 per row)
# - Filters hidden by default; shown only on button click
# - All calculations update with filtered data

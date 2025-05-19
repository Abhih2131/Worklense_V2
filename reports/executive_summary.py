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

    # --- KPI calculations must come BEFORE using variables! ---
    mask_active = (filtered_df['date_of_joining'] <= today) & (
        (filtered_df['date_of_exit'].isna()) | (filtered_df['date_of_exit'] > today)
    )
    active = mask_active.sum()

    leavers = filtered_df['date_of_exit'].between(fy_start, fy_end).sum()
    headcount_start = ((filtered_df['date_of_joining'] <= fy_start) &
        ((filtered_df['date_of_exit'].isna()) | (filtered_df['date_of_exit'] > fy_start))).sum()
    headcount_end = ((filtered_df['date_of_joining'] <= fy_end) &
        ((filtered_df['date_of_exit'].isna()) | (filtered_df['date_of_exit'] > fy_end))).sum()
    avg_headcount = (headcount_start + headcount_end) / 2 if (headcount_start + headcount_end) else 1
    attrition = (leavers / avg_headcount) * 100 if avg_headcount else 0

    joiners = filtered_df['date_of_joining'].between(fy_start, fy_end).sum()
    total_cost = filtered_df['total_ctc_pa'].sum()
    female = mask_active & (filtered_df['gender'] == 'Female')
    total_active = mask_active.sum()
    female_ratio = (female.sum() / total_active * 100) if total_active > 0 else 0
    avg_tenure = filtered_df['total_exp_yrs'].mean() if 'total_exp_yrs' in filtered_df else 0

    now = datetime.now()
    def calc_age(dob):
        if pd.isnull(dob):
            return None
        return (now - pd.to_datetime(dob)).days // 365
    avg_age = filtered_df['date_of_birth'].apply(calc_age).mean() if 'date_of_birth' in filtered_df else 0
    avg_total_exp = filtered_df['total_exp_yrs'].mean() if 'total_exp_yrs' in filtered_df else 0

    # --- Now create KPI list ---
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

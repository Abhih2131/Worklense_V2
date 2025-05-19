# reports/executive_summary.py

import streamlit as st
import pandas as pd
from datetime import datetime
from kpi_design import KPI_STYLE, format_kpi
from utils.data_handler import ensure_datetime

def run_report(data, config):
    st.title("Executive Summary")

    emp_df = data.get("employee_master", pd.DataFrame())
    filtered_df = emp_df.copy()
    filtered_df = ensure_datetime(filtered_df, ['date_of_joining', 'date_of_exit', 'date_of_birth'])

    today = pd.Timestamp.now().normalize()
    fy_start = pd.Timestamp('2025-04-01')
    fy_end = pd.Timestamp('2026-03-31')

    # Active Employees (as of today)
    mask_active = (filtered_df['date_of_joining'] <= today) & \
        ((filtered_df['date_of_exit'].isna()) | (filtered_df['date_of_exit'] > today))
    active = mask_active.sum()

    # Attrition Rate FY 2025-26
    leavers = filtered_df['date_of_exit'].between(fy_start, fy_end).sum()
    headcount_start = ((filtered_df['date_of_joining'] <= fy_start) &
        ((filtered_df['date_of_exit'].isna()) | (filtered_df['date_of_exit'] > fy_start))).sum()
    headcount_end = ((filtered_df['date_of_joining'] <= fy_end) &
        ((filtered_df['date_of_exit'].isna()) | (filtered_df['date_of_exit'] > fy_end))).sum()
    avg_headcount = (headcount_start + headcount_end) / 2 if (headcount_start + headcount_end) else 1
    attrition = (leavers / avg_headcount) * 100 if avg_headcount else 0

    # Joiners (FY 2025-26)
    joiners = filtered_df['date_of_joining'].between(fy_start, fy_end).sum()

    # Total Cost (INR)
    total_cost = filtered_df['total_ctc_pa'].sum()

    # Female Ratio (active as of today)
    female = mask_active & (filtered_df['gender'] == 'Female')
    total_active = mask_active.sum()
    female_ratio = (female.sum() / total_active * 100) if total_active > 0 else 0

    # Avg Tenure (years)
    avg_tenure = filtered_df['total_exp_yrs'].mean() if 'total_exp_yrs' in filtered_df else 0

    # Avg Age (years)
    now = datetime.now()
    def calc_age(dob):
        if pd.isnull(dob): return None
        return (now - pd.to_datetime(dob)).days // 365
    avg_age = filtered_df['date_of_birth'].apply(calc_age).mean() if 'date_of_birth' in filtered_df else 0

    # Avg Total Exp (years)
    avg_total_exp = filtered_df['total_exp_yrs'].mean() if 'total_exp_yrs' in filtered_df else 0

    # --- KPI Display Data ---
    kpis = [
        {"label": "Active Employees", "value": active, "type": "Integer"},
        {"label": "Attrition Rate (FY 25-26)", "value": attrition, "type": "Percentage"},
        {"label": "Joiners (FY 25-26)", "value": joiners, "type": "Integer"},
        {"label": "Total Cost (INR)", "value": total_cost, "type": "Currency"},
        {"label": "Female Ratio", "value": female_ratio, "type": "Percentage"},
        {"label": "Avg Tenure (yrs)", "value": avg_tenure, "type": "Years"},
        {"label": "Avg Age", "value": avg_age, "type": "Years"},
        {"label": "Avg Total Exp (yrs)", "value": avg_total_exp, "type": "Years"},
    ]

    for i in range(0, len(kpis), 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            if idx >= len(kpis): break
            kpi = kpis[idx]
            with cols[j]:
                st.markdown(
                    f"""
                    <div style="
                        background:{KPI_STYLE['background_color']};
                        box-shadow:{KPI_STYLE['box_shadow']};
                        border-radius:{KPI_STYLE['border_radius']};
                        padding:{KPI_STYLE['padding']};
                        width:{KPI_STYLE['box_width']}px;
                        height:{KPI_STYLE['box_height']}px;
                        text-align:center;
                        display:flex;
                        flex-direction:column;
                        justify-content:center;
                        align-items:center;">
                        <span style="font-size:{KPI_STYLE['font_size_label']};font-weight:{'bold' if KPI_STYLE['label_bold'] else 'normal'};">
                            {kpi['label']}
                        </span>
                        <span style="font-size:{KPI_STYLE['font_size_value']};color:{KPI_STYLE['value_color']};margin-top:10px;">
                            {format_kpi(kpi['value'], kpi['type'])}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.subheader("Charts")
    st.info("Charts will appear here in future releases.")
    st.button("Export KPIs to Excel (Coming Soon)")

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render_kpi_card(label, value):
    return f"""
    <div class="kpi-card">
        <div class="kpi-accent"></div>
        <span class="kpi-label">{label}</span>
        <span class="kpi-value">{value}</span>
    </div>
    """

def run_report(data, config):
    st.title("Executive Summary")

    filtered_df = data.get("employee_master", pd.DataFrame())
    today = pd.Timestamp.now().normalize()
    fy_start = pd.Timestamp('2025-04-01')
    fy_end = pd.Timestamp('2026-03-31')

    # KPIs calculation (same logic as before)
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

    # Format KPI values
    total_cost_display = f"₹{total_cost / 1e7:,.0f} Cr"
    attrition_display = f"{attrition:.1f}%"
    female_ratio_display = f"{female_ratio:.1f}%"
    avg_tenure_display = f"{avg_tenure:.1f} Yrs"
    avg_age_display = f"{avg_age:.1f} Yrs"
    avg_total_exp_display = f"{avg_total_exp:.1f} Yrs"

    kpis = [
        {"label": "Active Employees", "value": f"{int(active):,}"},
        {"label": "Attrition Rate (FY 25-26)", "value": attrition_display},
        {"label": "Joiners (FY 25-26)", "value": f"{int(joiners):,}"},
        {"label": "Total Cost (INR)", "value": total_cost_display},
        {"label": "Female Ratio", "value": female_ratio_display},
        {"label": "Avg Tenure", "value": avg_tenure_display},
        {"label": "Avg Age", "value": avg_age_display},
        {"label": "Avg Total Exp", "value": avg_total_exp_display},
    ]

    # Render KPI cards 4 per row
    for i in range(0, len(kpis), 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            if idx >= len(kpis):
                break
            kpi = kpis[idx]
            with cols[j]:
                st.markdown(render_kpi_card(kpi['label'], kpi['value']), unsafe_allow_html=True)

    st.subheader("Charts")

    # Chart 1: Manpower Growth (line chart)
    manpower_growth_data = prepare_manpower_growth_data(filtered_df)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Manpower Growth")
        render_line_chart(manpower_growth_data, x="FY", y="Headcount")

    # Chart 2: Manpower Cost Trend (bar chart)
    manpower_cost_data = prepare_manpower_cost_data(filtered_df)
    with col2:
        st.subheader("Manpower Cost Trend")
        render_bar_chart(manpower_cost_data, x="FY", y="Total Cost")

    # Additional charts placeholders
    # Repeat similar blocks as needed with st.columns for side-by-side

def prepare_manpower_growth_data(df):
    # Dummy example: group by FY and count active employees
    fy_data = {
        "FY": ["FY-2022", "FY-2023", "FY-2024", "FY-2025", "FY-2026"],
        "Headcount": [16000, 17000, 18000, 15000, 16800]
    }
    return pd.DataFrame(fy_data)

def prepare_manpower_cost_data(df):
    # Dummy example: group by FY and sum cost (in Cr)
    fy_data = {
        "FY": ["FY-2022", "FY-2023", "FY-2024", "FY-2025", "FY-2026"],
        "Total Cost": [2200, 2400, 2500, 2000, 2100]
    }
    return pd.DataFrame(fy_data)

def render_line_chart(df, x, y):
    fig = px.line(df, x=x, y=y)
    st.plotly_chart(fig, use_container_width=True)

def render_bar_chart(df, x, y):
    fig = px.bar(df, x=x, y=y)
    st.plotly_chart(fig, use_container_width=True)

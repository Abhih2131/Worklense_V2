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

    # --- Sidebar Chart Theme Selector ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Chart Theme")
    chart_theme = st.sidebar.selectbox(
        "Select Chart Theme",
        options=[
            "Classic Light",
            "Elegant Dark",
            "Presentation Mode",
            "Soft Pastel",
            "Pastel Elegance",
            "Minimalist White",
            "Balanced Classic",
            "Clean Grid"
        ],
        index=0,
        help="Choose how charts are styled"
    )
    theme_map = {
        "Classic Light": "plotly_white",
        "Elegant Dark": "plotly_dark",
        "Presentation Mode": "presentation",
        "Soft Pastel": "ggplot2",
        "Pastel Elegance": "seaborn",
        "Minimalist White": "simple_white",
        "Balanced Classic": "plotly",
        "Clean Grid": "xgridoff"
    }
    selected_template = theme_map[chart_theme]

    # KPI calculations
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

    charts = [
        ("Manpower Growth", prepare_manpower_growth_data, render_line_chart, {"x": "FY", "y": "Headcount"}),
        ("Manpower Cost Trend", prepare_manpower_cost_data, render_bar_chart, {"x": "FY", "y": "Total Cost"}),
        ("Attrition Trend", prepare_attrition_data, render_line_chart, {"x": "FY", "y": "Attrition %"}),
        ("Gender Diversity", prepare_gender_data, render_donut_chart, {"names": "Gender", "values": "Count"}),
        ("Age Distribution", prepare_age_distribution, render_pie_chart, {"names": "Age Group", "values": "Count"}),
        ("Tenure Distribution", prepare_tenure_distribution, render_pie_chart, {"names": "Tenure Group", "values": "Count"}),
        ("Total Experience Distribution", prepare_experience_distribution, render_bar_chart, {"x": "Experience Group", "y": "Count"}),
        ("Transfer % Trend", prepare_transfer_trend, render_line_chart, {"x": "FY", "y": "Transfer %"}),
        ("Top Talent Ratio", prepare_top_talent_data, render_pie_chart, {"names": "Talent", "values": "Count"}),
        ("Performance Distribution", prepare_performance_distribution, render_bell_curve, {"x": "Rating"}),
        ("Education Type Distribution", prepare_education_distribution, render_donut_chart, {"names": "Qualification", "values": "Count"}),
        ("Salary Distribution", prepare_salary_distribution, render_box_plot, {"y": "CTC"}),
    ]

    for i in range(0, len(charts), 2):
        cols = st.columns(2)
        for j in range(2):
            idx = i + j
            if idx >= len(charts):
                break
            title, prep_func, render_func, params = charts[idx]
            data_chart = prep_func(filtered_df)
            with cols[j]:
                st.subheader(title)
                render_func(data_chart, **params)

# Data prep and render functions same as previous example...

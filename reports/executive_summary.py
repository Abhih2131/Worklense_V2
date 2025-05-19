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
        ("Manpower Growth", prepare_manpower_growth_data, render_line_chart, {"x":"FY", "y":"Headcount"}),
        ("Manpower Cost Trend", prepare_manpower_cost_data, render_bar_chart, {"x":"FY", "y":"Total Cost"}),
        ("Attrition Trend", prepare_attrition_data, render_line_chart, {"x":"FY", "y":"Attrition %"}),
        ("Gender Diversity", prepare_gender_data, render_donut_chart, {"names":"Gender", "values":"Count"}),
        ("Age Distribution", prepare_age_distribution, render_pie_chart, {"names":"Age Group", "values":"Count"}),
        ("Tenure Distribution", prepare_tenure_distribution, render_pie_chart, {"names":"Tenure Group", "values":"Count"}),
        ("Total Experience Distribution", prepare_experience_distribution, render_bar_chart, {"x":"Experience Group", "y":"Count"}),
        ("Transfer % Trend", prepare_transfer_trend, render_line_chart, {"x":"FY", "y":"Transfer %"}),
        ("Top Talent Ratio", prepare_top_talent_data, render_pie_chart, {"names":"Talent", "values":"Count"}),
        ("Performance Distribution", prepare_performance_distribution, render_bell_curve, {"x":"Rating"}),
        ("Education Type Distribution", prepare_education_distribution, render_donut_chart, {"names":"Qualification", "values":"Count"}),
        ("Salary Distribution", prepare_salary_distribution, render_box_plot, {"y":"CTC"}),
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

# Data prep functions (same dummy data as before)

def prepare_manpower_growth_data(df):
    return pd.DataFrame({"FY":["FY-22","FY-23","FY-24","FY-25","FY-26"],"Headcount":[16000,17000,18000,15000,16800]})

def prepare_manpower_cost_data(df):
    return pd.DataFrame({"FY":["FY-22","FY-23","FY-24","FY-25","FY-26"],"Total Cost":[2200,2400,2500,2000,2100]})

def prepare_attrition_data(df):
    return pd.DataFrame({"FY":["FY-22","FY-23","FY-24","FY-25","FY-26"],"Attrition %":[12,15,13,16,14]})

def prepare_gender_data(df):
    return pd.DataFrame({"Gender":["Female","Male"],"Count":[5000,7000]})

def prepare_age_distribution(df):
    return pd.DataFrame({"Age Group":["20-30","31-40","41-50","51-60"],"Count":[3000,4000,2500,1500]})

def prepare_tenure_distribution(df):
    return pd.DataFrame({"Tenure Group":["0-1","1-3","3-5","5-10","10+"],"Count":[1000,3000,2500,3500,1000]})

def prepare_experience_distribution(df):
    return pd.DataFrame({"Experience Group":["<1","1-3","3-5","5-10","10+"],"Count":[1200,2800,2600,3100,1300]})

def prepare_transfer_trend(df):
    return pd.DataFrame({"FY":["FY-22","FY-23","FY-24","FY-25","FY-26"],"Transfer %":[5,6,7,6,7]})

def prepare_top_talent_data(df):
    return pd.DataFrame({"Talent":["Top","Others"],"Count":[1500,6500]})

def prepare_performance_distribution(df):
    return pd.DataFrame({"Rating":[1,2,3,4,5],"Count":[100,200,500,700,500]})

def prepare_education_distribution(df):
    return pd.DataFrame({"Qualification":["UG","PG","Diploma","PhD"],"Count":[4000,3500,2000,500]})

def prepare_salary_distribution(df):
    return pd.DataFrame({"CTC":[1,2,3,4,5,6,7,8,9,10,11,12]})

# Plotly renderers

def render_line_chart(df, x, y):
    fig = px.line(df, x=x, y=y)
    st.plotly_chart(fig, use_container_width=True)

def render_bar_chart(df, x, y):
    fig = px.bar(df, x=x, y=y)
    st.plotly_chart(fig, use_container_width=True)

def render_pie_chart(df, names, values):
    fig = px.pie(df, names=names, values=values)
    st.plotly_chart(fig, use_container_width=True)

def render_donut_chart(df, names, values):
    fig = px.pie(df, names=names, values=values, hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

def render_box_plot(df, y):
    fig = px.box(df, y=y)
    st.plotly_chart(fig, use_container_width=True)

def render_bell_curve(df, x):
    fig = px.histogram(df, x=x, nbins=20)
    st.plotly_chart(fig, use_container_width=True)

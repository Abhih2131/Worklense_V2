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
        ("Manpower Growth", prepare_manpower_growth_data, render_line_chart),
        ("Manpower Cost Trend", prepare_manpower_cost_data, render_bar_chart),
        ("Attrition Trend", prepare_attrition_data, render_line_chart),
        ("Gender Diversity", prepare_gender_data, render_donut_chart),
        ("Age Distribution", prepare_age_distribution, render_pie_chart),
        ("Tenure Distribution", prepare_tenure_distribution, render_pie_chart),
        ("Total Experience Distribution", prepare_experience_distribution, render_bar_chart),
        ("Transfer % Trend", prepare_transfer_trend, render_line_chart),
        ("Top Talent Ratio", prepare_top_talent_data, render_pie_chart),
        ("Performance Distribution", prepare_performance_distribution, render_bell_curve),
        ("Education Type Distribution", prepare_education_distribution, render_donut_chart),
        ("Salary Distribution", prepare_salary_distribution, render_box_plot),
    ]

    for i in range(0, len(charts), 2):
        cols = st.columns(2)
        for j in range(2):
            idx = i + j
            if idx >= len(charts):
                break
            title, prep_func, render_func = charts[idx]
            data_chart = prep_func(filtered_df)
            with cols[j]:
                st.subheader(title)
                render_func(data_chart)

# Placeholder data prep functions
def prepare_manpower_growth_data(df): return pd.DataFrame({"FY":["FY-22","FY-23"],"Headcount":[16000,17000]})
def prepare_manpower_cost_data(df): return pd.DataFrame({"FY":["FY-22","FY-23"],"Total Cost":[2200,2400]})
def prepare_attrition_data(df): return pd.DataFrame({"FY":["FY-22","FY-23"],"Attrition %":[12,15]})
def prepare_gender_data(df): return pd.DataFrame({"Gender":["Female","Male"],"Count":[50,50]})
def prepare_age_distribution(df): return pd.DataFrame({"Age Group":["20-30","31-40"],"Count":[300,200]})
def prepare_tenure_distribution(df): return pd.DataFrame({"Tenure Group":["0-1","1-3"],"Count":[150,350]})
def prepare_experience_distribution(df): return pd.DataFrame({"Experience Group":["0-5","5-10"],"Count":[400,100]})
def prepare_transfer_trend(df): return pd.DataFrame({"FY":["FY-22","FY-23"],"Transfer %":[2,3]})
def prepare_top_talent_data(df): return pd.DataFrame({"Talent":["Top","Others"],"Count":[100,400]})
def prepare_performance_distribution(df): return pd.DataFrame({"Rating":[1,2,3,4,5],"Count":[5,15,25,30,25]})
def prepare_education_distribution(df): return pd.DataFrame({"Qualification":["UG","PG"],"Count":[250,150]})
def prepare_salary_distribution(df): return pd.DataFrame({"CTC":[1,2,3,4,5,6,7,8,9,10]})

# Placeholder render functions using Plotly
def render_line_chart(df, x="FY", y="Headcount"):
    fig = px.line(df, x=x, y=y)
    st.plotly_chart(fig, use_container_width=True)

def render_bar_chart(df, x="FY", y="Total Cost"):
    fig = px.bar(df, x=x, y=y)
    st.plotly_chart(fig, use_container_width=True)

def render_pie_chart(df, names="Age Group", values="Count"):
    fig = px.pie(df, names=names, values=values)
    st.plotly_chart(fig, use_container_width=True)

def render_donut_chart(df, names="Gender", values="Count"):
    fig = px.pie(df, names=names, values=values, hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

def render_box_plot(df, y="CTC"):
    fig = px.box(df, y=y)
    st.plotly_chart(fig, use_container_width=True)

def render_bell_curve(df, x="Rating"):
    fig = px.histogram(df, x=x, nbins=20)
    st.plotly_chart(fig, use_container_width=True)

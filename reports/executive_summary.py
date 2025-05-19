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

# Data preparation functions (simplified for demo, customize as needed)
def prepare_manpower_growth_data(df):
    df = df.copy()
    df['FY'] = df['date_of_joining'].dt.year.apply(lambda y: f"FY-{str(y)[-2:]}")
    grouped = df.groupby('FY').size().reset_index(name='Headcount')
    return grouped.sort_values('FY')

def prepare_manpower_cost_data(df):
    df = df.copy()
    df['FY'] = df['date_of_joining'].dt.year.apply(lambda y: f"FY-{str(y)[-2:]}")
    grouped = df.groupby('FY')['total_ctc_pa'].sum().reset_index(name='Total Cost')
    return grouped.sort_values('FY')

def prepare_attrition_data(df):
    df = df.copy()
    df['FY'] = df['date_of_exit'].dt.year.apply(lambda y: f"FY-{str(y)[-2:]}" if pd.notnull(y) else None)
    attrition_df = df.groupby('FY').size().reset_index(name='Leavers')
    headcount_df = df.groupby('FY').size().reset_index(name='Headcount')
    merged = pd.merge(attrition_df, headcount_df, on='FY')
    merged['Attrition %'] = (merged['Leavers'] / merged['Headcount']) * 100
    return merged[['FY', 'Attrition %']].sort_values('FY')

def prepare_gender_data(df):
    df = df.copy()
    df = df[df['date_of_exit'].isna()]
    counts = df['gender'].value_counts().reset_index()
    counts.columns = ['Gender', 'Count']
    return counts

def prepare_age_distribution(df):
    df = df.copy()
    df = df[df['date_of_exit'].isna()]
    bins = [0, 20, 25, 30, 35, 40, 45, 50, 55, 60, 100]
    labels = ['<20', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60+']
    df['Age Group'] = pd.cut(df['date_of_birth'].apply(lambda dob: (pd.Timestamp.now() - dob).days // 365 if pd.notnull(dob) else 0), bins=bins, labels=labels)
    counts = df['Age Group'].value_counts().reset_index()
    counts.columns = ['Age Group', 'Count']
    return counts.sort_values('Age Group')

def prepare_tenure_distribution(df):
    df = df.copy()
    df = df[df['date_of_exit'].isna()]
    bins = [0, 0.5, 1, 3, 5, 10, 40]
    labels = ['0-6 Months', '6-12 Months', '1-3 Years', '3-5 Years', '5-10 Years', '10+ Years']
    df['Tenure Group'] = pd.cut(df['total_exp_yrs'], bins=bins, labels=labels)
    counts = df['Tenure Group'].value_counts().reset_index()
    counts.columns = ['Tenure Group', 'Count']
    return counts.sort_values('Tenure Group')

def prepare_experience_distribution(df):
    df = df.copy()
    df = df[df['date_of_exit'].isna()]
    bins = [0, 1, 3, 5, 10, 40]
    labels = ['<1 Year', '1-3 Years', '3-5 Years', '5-10 Years', '10+ Years']
    df['Experience Group'] = pd.cut(df['total_exp_yrs'], bins=bins, labels=labels)
    counts = df['Experience Group'].value_counts().reset_index()
    counts.columns = ['Experience Group', 'Count']
    return counts.sort_values('Experience Group')

def prepare_transfer_trend(df):
    if 'transfer_date' not in df.columns or 'transfer_flag' not in df.columns:
        return pd.DataFrame(columns=['FY', 'Transfer %'])
    df = df.copy()
    df['FY'] = df['transfer_date'].dt.year.apply(lambda y: f"FY-{str(y)[-2:]}" if pd.notnull(y) else None)
    transfer_counts = df[df['transfer_flag'] == True].groupby('FY').size()
    total_counts = df.groupby('FY').size()
    transfer_percent = (transfer_counts / total_counts * 100).reset_index(name='Transfer %').fillna(0)
    return transfer_percent.sort_values('FY')

def prepare_top_talent_data(df):
    if 'is_top_talent' not in df.columns:
        return pd.DataFrame({'Talent': ['Top Talent', 'Others'], 'Count': [0, len(df)]})
    df = df.copy()
    counts = df['is_top_talent'].map({True: 'Top Talent', False: 'Others'}).value_counts().reset_index()
    counts.columns = ['Talent', 'Count']
    return counts

def prepare_performance_distribution(df):
    if 'performance_rating' not in df.columns:
        return pd.DataFrame(columns=['Rating'])
    df = df.copy()
    return df[['performance_rating']].dropna()

def prepare_education_distribution(df):
    df = df.copy()
    df = df[df['date_of_exit'].isna()]
    counts = df['qualification_type'].value_counts().reset_index()
    counts.columns = ['Qualification', 'Count']
    return counts

def prepare_salary_distribution(df):
    df = df.copy()
    df = df[df['date_of_exit'].isna()]
    return df[['total_ctc_pa']].dropna()

# Chart rendering functions
def render_line_chart(df, x, y):
    fig = px.line(df, x=x, y=y)
    st.plotly_chart(fig, use_container_width=True)

def render_bar_chart(df, x, y):
    fig = px.bar(df, x=x, y=y)
    st.plotly_chart(fig, use_container_width=True)

def render_pie_chart(df, names, values):
    fig = px.pie(df, names=names, values=values, hole=0)
    st.plotly_chart(fig, use_container_width=True)

def render_donut_chart(df, names, values):
    fig = px.pie(df, names=names, values=values, hole=0.5)
    st.plotly_chart(fig, use_container_width=True)

def render_bell_curve(df, col):
    import plotly.figure_factory as ff
    data = [df[col].dropna()]
    fig = ff.create_distplot(data, [col], show_hist=False, show_rug=False)
    st.plotly_chart(fig, use_container_width=True)

def run_report(data, config):
    st.title("Executive Summary")

    df = data.get("employee_master", pd.DataFrame())

    today = pd.Timestamp.now().normalize()
    fy_start = pd.Timestamp('2025-04-01')
    fy_end = pd.Timestamp('2026-03-31')

    # KPIs
    mask_active = (df['date_of_joining'] <= today) & ((df['date_of_exit'].isna()) | (df['date_of_exit'] > today))
    active = mask_active.sum()
    leavers = df['date_of_exit'].between(fy_start, fy_end).sum()
    headcount_start = ((df['date_of_joining'] <= fy_start) & ((df['date_of_exit'].isna()) | (df['date_of_exit'] > fy_start))).sum()
    headcount_end = ((df['date_of_joining'] <= fy_end) & ((df['date_of_exit'].isna()) | (df['date_of_exit'] > fy_end))).sum()
    avg_headcount = (headcount_start + headcount_end) / 2 if (headcount_start + headcount_end) else 1
    attrition = (leavers / avg_headcount) * 100 if avg_headcount else 0
    joiners = df['date_of_joining'].between(fy_start, fy_end).sum()
    total_cost = df['total_ctc_pa'].sum()
    female = mask_active & (df['gender'] == 'Female')
    total_active = mask_active.sum()
    female_ratio = (female.sum() / total_active * 100) if total_active > 0 else 0
    avg_tenure = df['total_exp_yrs'].mean() if 'total_exp_yrs' in df else 0

    now = datetime.now()
    def calc_age(dob):
        if pd.isnull(dob):
            return None
        return (now - pd.to_datetime(dob)).days // 365

    avg_age = df['date_of_birth'].apply(calc_age).mean() if 'date_of_birth' in df else 0
    avg_total_exp = df['total_exp_yrs'].mean() if 'total_exp_yrs' in df else 0

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

    # Show KPIs (4 per row)
    for i in range(0, len(kpis), 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            if idx >= len(kpis):
                break
            kpi = kpis[idx]
            with cols[j]:
                st.markdown(render_kpi_card(kpi['label'], kpi['value']), unsafe_allow_html=True)

    # Charts Data and Renderers list
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
        ("Performance Distribution", prepare_performance_distribution, render_bell_curve, "performance_rating"),
        ("Education Type Distribution", prepare_education_distribution, render_donut_chart, {"names": "Qualification", "values": "Count"}),
        ("Salary Distribution", prepare_salary_distribution, render_bell_curve, "total_ctc_pa"),
    ]

    # Render charts side-by-side in pairs
    for i in range(0, len(charts), 2):
        cols = st.columns(2)
        for j in range(2):
            idx = i + j
            if idx >= len(charts):
                break
            title, prepare_func, render_func, params = charts[idx]
            st.write(f"### {title}")
            df_chart = prepare_func(df)
            if isinstance(params, dict):
                render_func(df_chart, **params)
            else:
                render_func(df_chart, params)

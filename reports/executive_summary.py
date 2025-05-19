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

def prepare_manpower_growth_data(df):
    today = pd.Timestamp.now().normalize()
    years = [f"FY-{y}" for y in range(21, 26)]
    records = []
    for y in years:
        fy_year = int(y.split("-")[1]) + 2000
        end = pd.Timestamp(f"{fy_year+1}-03-31")
        headcount = df[(df['date_of_joining'] <= end) & ((df['date_of_exit'].isna()) | (df['date_of_exit'] > end))].shape[0]
        records.append({"FY": y, "Headcount": headcount})
    return pd.DataFrame(records)

def prepare_manpower_cost_data(df):
    years = [f"FY-{y}" for y in range(21, 26)]
    records = []
    for y in years:
        fy_year = int(y.split("-")[1]) + 2000
        end = pd.Timestamp(f"{fy_year+1}-03-31")
        total_cost = df[(df['date_of_joining'] <= end) & ((df['date_of_exit'].isna()) | (df['date_of_exit'] > end))]['total_ctc_pa'].sum()
        records.append({"FY": y, "Total Cost": total_cost/1e7})
    return pd.DataFrame(records)

def prepare_attrition_trend_data(df):
    years = [f"FY-{y}" for y in range(21, 26)]
    records = []
    for y in years:
        fy_year = int(y.split("-")[1]) + 2000
        start = pd.Timestamp(f"{fy_year}-04-01")
        end = pd.Timestamp(f"{fy_year+1}-03-31")
        leavers = df[df['date_of_exit'].between(start, end)].shape[0]
        headcount_start = df[(df['date_of_joining'] <= start) & ((df['date_of_exit'].isna()) | (df['date_of_exit'] > start))].shape[0]
        headcount_end = df[(df['date_of_joining'] <= end) & ((df['date_of_exit'].isna()) | (df['date_of_exit'] > end))].shape[0]
        avg_headcount = (headcount_start + headcount_end) / 2 if (headcount_start + headcount_end) else 1
        attrition = (leavers / avg_headcount) * 100 if avg_headcount else 0
        records.append({"FY": y, "Attrition %": attrition})
    return pd.DataFrame(records)

def prepare_gender_diversity_data(df):
    active_mask = (df['date_of_joining'] <= pd.Timestamp.now()) & ((df['date_of_exit'].isna()) | (df['date_of_exit'] > pd.Timestamp.now()))
    active_df = df[active_mask]
    counts = active_df['gender'].value_counts()
    return pd.DataFrame({"Gender": counts.index, "Count": counts.values})

def prepare_age_distribution_data(df):
    now = datetime.now()
    def calc_age(dob):
        if pd.isnull(dob):
            return None
        return (now - pd.to_datetime(dob)).days // 365
    df['age'] = df['date_of_birth'].apply(calc_age)
    bins = [0, 20, 25, 30, 35, 40, 45, 50, 55, 60, 100]
    labels = ['<20','20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
    counts = df['age_group'].value_counts().sort_index()
    return pd.DataFrame({"Age Group": counts.index, "Count": counts.values})

def prepare_tenure_distribution_data(df):
    bins = [0,0.5,1,3,5,10,100]
    labels = ['0-6 Months','6-12 Months','1-3 Years','3-5 Years','5-10 Years','10+ Years']
    df['tenure_group'] = pd.cut(df['total_exp_yrs'], bins=bins, labels=labels, right=False)
    counts = df['tenure_group'].value_counts().sort_index()
    return pd.DataFrame({"Tenure": counts.index, "Count": counts.values})

def prepare_total_experience_distribution_data(df):
    bins = [0,5,10,15,20,100]
    labels = ['0-5','6-10','11-15','16-20','20+']
    df['total_exp_group'] = pd.cut(df['total_exp_yrs'], bins=bins, labels=labels, right=False)
    counts = df['total_exp_group'].value_counts().sort_index()
    return pd.DataFrame({"Total Exp": counts.index, "Count": counts.values})

def prepare_transfer_trend_data(df):
    years = [f"FY-{y}" for y in range(21, 26)]
    records = []
    for y in years:
        val = 5 + (y.__hash__() % 10)
        records.append({"FY": y, "Transfer %": val})
    return pd.DataFrame(records)

def prepare_top_talent_ratio_data(df):
    top_talent = df[df['total_exp_yrs'] > 10].shape[0]
    others = df.shape[0] - top_talent
    return pd.DataFrame({"Talent": ["Top Talent", "Others"], "Count": [top_talent, others]})

def prepare_performance_distribution_data(df):
    return df[['performance_rating']].dropna()

def prepare_salary_distribution_data(df):
    return df[['total_ctc_pa']].dropna()

# Chart render functions
def render_line_chart(df, x, y, template):
    fig = px.line(df, x=x, y=y, template=template, markers=True, text=df[y])
    fig.update_traces(textposition='top center')
    st.plotly_chart(fig, use_container_width=True)

def render_bar_chart(df, x, y, template):
    fig = px.bar(df, x=x, y=y, template=template, text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

def render_pie_chart(df, names, values, template):
    fig = px.pie(df, names=names, values=values, template=template, textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

def render_donut_chart(df, names, values, template):
    fig = px.pie(df, names=names, values=values, hole=0.5, template=template, textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

def render_bell_curve(df, col, template):
    import plotly.figure_factory as ff
    data = df[col].dropna()
    if data.empty:
        st.info("No data available for bell curve.")
        return
    fig = ff.create_distplot([data], [col], show_hist=False, show_rug=False)
    fig.update_layout(template=template)
    st.plotly_chart(fig, use_container_width=True)

def run_report(data, config):
    st.title("Executive Summary")
    filtered_df = data.get("employee_master", pd.DataFrame())

    # Place Chart Theme just below Filters, remove gap
    st.sidebar.markdown("### Chart Theme", unsafe_allow_html=True)
    chart_theme = st.sidebar.selectbox(
        "Select Chart Theme",
        options=["plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"],
        index=0
    )

    # KPI Section (same as before)
    today = pd.Timestamp.now().normalize()
    fy_start = pd.Timestamp('2025-04-01')
    fy_end = pd.Timestamp('2026-03-31')
    mask_active = (filtered_df['date_of_joining'] <= today) & (
        (filtered_df['date_of_exit'].isna()) | (filtered_df['date_of_exit'] > today)
    )
    active = mask_active.sum

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render_kpi_card(label, value):
    return f"""
    <div style='background:#fff;border-radius:22px;box-shadow:0 4px 16px rgba(44,58,92,.12);padding:16px 10px 14px 26px;min-height:78px;max-width:330px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;margin-bottom:18px;'>
        <div style='font-weight:700;font-size:19px;color:#222;margin-bottom:3px'>{label}</div>
        <div style='font-size:30px;font-weight:800;color:#1a237e;margin-top:2px;'>{value}</div>
    </div>
    """

def get_last_fy_list(current_fy, n=5):
    return [f"FY-{str(current_fy-i)[-2:]}" for i in range(n-1,-1,-1)]

def theme_selector():
    themes = {
        "Light": "#f7f9fb",
        "Classic Blue": "#eef4ff",
        "Dark": "#1a2234"
    }
    selected = st.sidebar.selectbox("Theme Selector", list(themes.keys()))
    bg_color = themes[selected]
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {bg_color}; }}
        </style>
    """, unsafe_allow_html=True)

    plotly_themes = {
        "Default": "plotly",
        "White Classic": "plotly_white",
        "GGPlot Style": "ggplot2",
        "Seaborn Style": "seaborn",
        "Simple White": "simple_white",
        "Presentation": "presentation",
        "Grid On": "gridon",
        "No Theme (None)": "none"
    }
    plotly_theme_label = st.sidebar.selectbox(
        "Chart Style (Plotly Theme)",
        options=list(plotly_themes.keys()),
        index=0
    )
    st.session_state["plotly_template"] = plotly_themes[plotly_theme_label]

def prepare_manpower_growth_data(df, fy_list):
    if 'date_of_joining' not in df.columns: return pd.DataFrame(columns=['FY','Headcount'])
    df = df.copy()
    df['FY'] = pd.to_datetime(df['date_of_joining'], errors='coerce').dt.year.apply(lambda y: f"FY-{str(y)[-2:]}" if pd.notnull(y) else None)
    grouped = df.groupby('FY').size().reset_index(name='Headcount')
    grouped = grouped[grouped['FY'].isin(fy_list)]
    grouped = grouped.set_index('FY').reindex(fy_list).reset_index().fillna(0)
    return grouped

def prepare_manpower_cost_data(df, fy_list):
    if 'date_of_joining' not in df.columns or 'total_ctc_pa' not in df.columns: return pd.DataFrame(columns=['FY','Total Cost'])
    df = df.copy()
    df['FY'] = pd.to_datetime(df['date_of_joining'], errors='coerce').dt.year.apply(lambda y: f"FY-{str(y)[-2:]}" if pd.notnull(y) else None)
    grouped = df.groupby('FY')['total_ctc_pa'].sum().reset_index(name='Total Cost')
    grouped = grouped[grouped['FY'].isin(fy_list)]
    grouped = grouped.set_index('FY').reindex(fy_list).reset_index().fillna(0)
    return grouped

def prepare_attrition_data(df, fy_list):
    if 'date_of_exit' not in df.columns: return pd.DataFrame(columns=['FY','Attrition %'])
    df = df.copy()
    df['FY'] = pd.to_datetime(df['date_of_exit'], errors='coerce').dt.year.apply(lambda y: f"FY-{str(y)[-2:]}" if pd.notnull(y) else None)
    attrition_df = df[df['date_of_exit'].notna()].groupby('FY').size().reset_index(name='Leavers')
    headcount_df = df.groupby('FY').size().reset_index(name='Headcount')
    merged = pd.merge(attrition_df, headcount_df, on='FY', how='left')
    merged['Attrition %'] = (merged['Leavers'] / merged['Headcount']) * 100
    merged = merged[merged['FY'].isin(fy_list)]
    merged = merged.set_index('FY').reindex(fy_list).reset_index().fillna(0)
    return merged[['FY', 'Attrition %']]

def prepare_gender_data(df):
    if 'gender' not in df.columns: return pd.DataFrame(columns=['Gender','Count'])
    df = df.copy()
    if 'date_of_exit' in df.columns:
        df = df[df['date_of_exit'].isna()]
    counts = df['gender'].value_counts().reset_index()
    counts.columns = ['Gender', 'Count']
    return counts

def prepare_age_distribution(df):
    if 'date_of_birth' not in df.columns: return pd.DataFrame(columns=['Age Group','Count'])
    df = df.copy()
    if 'date_of_exit' in df.columns:
        df = df[df['date_of_exit'].isna()]
    bins = [0, 20, 25, 30, 35, 40, 45, 50, 55, 60, 100]
    labels = ['<20', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60+']
    df['Age'] = df['date_of_birth'].apply(lambda dob: (pd.Timestamp.now() - pd.to_datetime(dob, errors='coerce')).days // 365 if pd.notnull(dob) else 0)
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels)
    counts = df['Age Group'].value_counts().reset_index()
    counts.columns = ['Age Group', 'Count']
    return counts.sort_values('Age Group')

def prepare_tenure_distribution(df):
    if 'total_exp_yrs' not in df.columns: return pd.DataFrame(columns=['Tenure Group','Count'])
    df = df.copy()
    if 'date_of_exit' in df.columns:
        df = df[df['date_of_exit'].isna()]
    bins = [0, 0.5, 1, 3, 5, 10, 40]
    labels = ['0-6 Months', '6-12 Months', '1-3 Years', '3-5 Years', '5-10 Years', '10+ Years']
    df['Tenure Group'] = pd.cut(df['total_exp_yrs'], bins=bins, labels=labels)
    counts = df['Tenure Group'].value_counts().reset_index()
    counts.columns = ['Tenure Group', 'Count']
    return counts.sort_values('Tenure Group')

def prepare_experience_distribution(df):
    if 'total_exp_yrs' not in df.columns: return pd.DataFrame(columns=['Experience Group','Count'])
    df = df.copy()
    if 'date_of_exit' in df.columns:
        df = df[df['date_of_exit'].isna()]
    bins = [0, 1, 3, 5, 10, 40]
    labels = ['<1 Year', '1-3 Years', '3-5 Years', '5-10 Years', '10+ Years']
    df['Experience Group'] = pd.cut(df['total_exp_yrs'], bins=bins, labels=labels)
    counts = df['Experience Group'].value_counts().reset_index()
    counts.columns = ['Experience Group', 'Count']
    return counts.sort_values('Experience Group')

def prepare_education_distribution(df):
    if 'qualification_type' not in df.columns: return pd.DataFrame(columns=['Qualification','Count'])
    df = df.copy()
    if 'date_of_exit' in df.columns:
        df = df[df['date_of_exit'].isna()]
    counts = df['qualification_type'].value_counts().reset_index()
    counts.columns = ['Qualification', 'Count']
    return counts

def render_line_chart(df, x, y):
    template = st.session_state.get("plotly_template", "plotly")
    if df.empty or x not in df.columns or y not in df.columns: st.write("No Data"); return
    fig = px.line(df, x=x, y=y, markers=True, template=template)
    st.plotly_chart(fig, use_container_width=True)

def render_bar_chart(df, x, y):
    template = st.session_state.get("plotly_template", "plotly")
    if df.empty or x not in df.columns or y not in df.columns: st.write("No Data"); return
    fig = px.bar(df, x=x, y=y, template=template)
    st.plotly_chart(fig, use_container_width=True)

def render_pie_chart(df, names, values):
    template = st.session_state.get("plotly_template", "plotly")
    if df.empty or names not in df.columns or values not in df.columns: st.write("No Data"); return
    fig = px.pie(df, names=names, values=values, hole=0, template=template)
    st.plotly_chart(fig, use_container_width=True)

def render_donut_chart(df, names, values):
    template = st.session_state.get("plotly_template", "plotly")
    if df.empty or names not in df.columns or values not in df.columns: st.write("No Data"); return
    fig = px.pie(df, names=names, values=values, hole=0.5, template=template)
    st.plotly_chart(fig, use_container_width=True)

def run_report(data, config):
    theme_selector()
    st.markdown(
        """
        <style>
            .block-container {padding-top:2.1rem;}
        </style>
        """, unsafe_allow_html=True
    )
    st.title("Executive Summary")
    df = data.get("employee_master", pd.DataFrame())
    now = datetime.now()
    current_fy = now.year + 1 if now.month >= 4 else now.year
    fy_list = get_last_fy_list(current_fy, n=5)

    today = pd.Timestamp.now().normalize()
    fy_start = pd.Timestamp(f"{current_fy-1}-04-01")
    fy_end = pd.Timestamp(f"{current_fy}-03-31")

    mask_active = (df['date_of_joining'] <= today) & ((df['date_of_exit'].isna()) | (df['date_of_exit'] > today))
    active = mask_active.sum()
    leavers = df['date_of_exit'].between(fy_start, fy_end).sum() if 'date_of_exit' in df.columns else 0
    headcount_start = ((df['date_of_joining'] <= fy_start) & ((df['date_of_exit'].isna()) | (df['date_of_exit'] > fy_start))).sum()
    headcount_end = ((df['date_of_joining'] <= fy_end) & ((df['date_of_exit'].isna()) | (df['date_of_exit'] > fy_end))).sum()
    avg_headcount = (headcount_start + headcount_end) / 2 if (headcount_start + headcount_end) else 1
    attrition = (leavers / avg_headcount) * 100 if avg_headcount else 0
    joiners = df['date_of_joining'].between(fy_start, fy_end).sum() if 'date_of_joining' in df.columns else 0
    total_cost = df['total_ctc_pa'].sum() if 'total_ctc_pa' in df.columns else 0
    female = mask_active & (df['gender'] == 'Female') if 'gender' in df.columns else 0
    total_active = mask_active.sum()
    female_ratio = (female.sum() / total_active * 100) if isinstance(female, pd.Series) and total_active > 0 else 0
    avg_tenure = df['total_exp_yrs'].mean() if 'total_exp_yrs' in df.columns else 0

    def calc_age(dob):
        if pd.isnull(dob): return None
        return (now - pd.to_datetime(dob, errors='coerce')).days // 365
    avg_age = df['date_of_birth'].apply(calc_age).mean() if 'date_of_birth' in df.columns else 0
    avg_total_exp = df['total_exp_yrs'].mean() if 'total_exp_yrs' in df.columns else 0

    total_cost_display = f"₹{total_cost / 1e7:,.0f} Cr"
    attrition_display = f"{attrition:.1f}%"
    female_ratio_display = f"{female_ratio:.1f}%"
    avg_tenure_display = f"{avg_tenure:.1f} Yrs"
    avg_age_display = f"{avg_age:.1f} Yrs"
    avg_total_exp_display = f"{avg_total_exp:.1f} Yrs"

    kpis = [
        {"label": "Active Employees", "value": f"{int(active):,}"},
        {"label": f"Attrition Rate (FY {str(current_fy-1)[-2:]}-{str(current_fy)[-2:]})", "value": attrition_display},
        {"label": f"Joiners (FY {str(current_fy-1)[-2:]}-{str(current_fy)[-2:]})", "value": f"{int(joiners):,}"},
        {"label": "Total Cost (INR)", "value": total_cost_display},
        {"label": "Female Ratio", "value": female_ratio_display},
        {"label": "Avg Tenure", "value": avg_tenure_display},
        {"label": "Avg Age", "value": avg_age_display},
        {"label": "Avg Total Exp", "value": avg_total_exp_display},
    ]

    for i in range(0, len(kpis), 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            if idx >= len(kpis): break
            kpi = kpis[idx]
            with cols[j]:
                st.markdown(render_kpi_card(kpi['label'], kpi['value']), unsafe_allow_html=True)

    charts = [
        ("Manpower Growth", lambda df: prepare_manpower_growth_data(df, fy_list), render_line_chart, {"x": "FY", "y": "Headcount"}),
        ("Manpower Cost Trend", lambda df: prepare_manpower_cost_data(df, fy_list), render_bar_chart, {"x": "FY", "y": "Total Cost"}),
        ("Attrition Trend", lambda df: prepare_attrition_data(df, fy_list), render_line_chart, {"x": "FY", "y": "Attrition %"}),
        ("Gender Diversity", prepare_gender_data, render_donut_chart, {"names": "Gender", "values": "Count"}),
        ("Age Distribution", prepare_age_distribution, render_pie_chart, {"names": "Age Group", "values": "Count"}),
        ("Tenure Distribution", prepare_tenure_distribution, render_pie_chart, {"names": "Tenure Group", "values": "Count"}),
        ("Total Experience Distribution", prepare_experience_distribution, render_bar_chart, {"x": "Experience Group", "y": "Count"}),
        ("Education Type Distribution", prepare_education_distribution, render_donut_chart, {"names": "Qualification", "values": "Count"}),
    ]

    for i in range(0, len(charts), 2):
        cols = st.columns(2, gap="large")
        for j in range(2):
            idx = i + j
            if idx >= len(charts): break
            title, prepare_func, render_func, params = charts[idx]
            with cols[j]:
                st.markdown(f"##### {title}")
                df_chart = prepare_func(df)
                if isinstance(params, dict):
                    render_func(df_chart, **params)
                else:
                    render_func(df_chart, params)

# Run command:
# streamlit run app.py

# UAT Checklist:
# - KPIs show with design as required.
# - 5-year charts for Manpower, Cost, Attrition.
# - Plotly chart theme selector working.
# - All 8 charts display, 2 per row.
# - Layout and data correct.

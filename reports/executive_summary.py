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
    years = [f"FY-{y}" for y in range(21, 26)]
    records = []
    for y in years:
        fy_year = int(y.split("-")[1]) + 2000
        end = pd.Timestamp(f"{fy_year+1}-03-31")
        headcount = df[(df['date_of_joining'] <= end) & ((df['date_of_exit'].isna()) | (df['date_of_exit'] > end))].shape[0]
        records.append({"FY": y, "Headcount": headcount})
    return pd.DataFrame(records)

def render_line_chart(df, x, y, template):
    fig = px.line(df, x=x, y=y, template=template, markers=True, text=df[y])
    fig.update_traces(textposition='top center')
    st.plotly_chart(fig, use_container_width=True)

def run_report(data, config):
    st.title("Executive Summary")
    filtered_df = data.get("employee_master", pd.DataFrame())
    st.write("Data shape:", filtered_df.shape)
    st.write(filtered_df.head())

    # Chart Theme
    chart_theme = st.sidebar.selectbox(
        "Select Chart Theme",
        options=["plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"],
        index=0
    )

    # Show simple KPI for testing
    st.header("KPI Test")
    st.markdown(render_kpi_card("Active Employees", str(filtered_df.shape[0])), unsafe_allow_html=True)

    # Show one test chart
    st.header("Test Manpower Growth Chart")
    df_chart = prepare_manpower_growth_data(filtered_df)
    render_line_chart(df_chart, x="FY", y="Headcount", template=chart_theme)

    # Add more charts here when you confirm data works

# End of file

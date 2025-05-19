import streamlit as st
import pandas as pd
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

    # KPI calculations (same as before)
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
                st.markdown(
                    render_kpi_card(kpi['label'], kpi['value']),
                    unsafe_allow_html=True
                )

    st.subheader("Charts")

    # Chart rendering calls (fixed types as per final list)

    # 1. Manpower Growth (line chart)
    manpower_growth_data = prepare_manpower_growth_data(filtered_df)
    render_line_chart(manpower_growth_data, x="FY", y="Headcount", title="Manpower Growth")

    # 2. Manpower Cost Trend (bar chart)
    manpower_cost_data = prepare_manpower_cost_data(filtered_df)
    render_bar_chart(manpower_cost_data, x="FY", y="Total Cost", title="Manpower Cost Trend")

    # 3. Attrition Trend (line chart)
    attrition_data = prepare_attrition_data(filtered_df)
    render_line_chart(attrition_data, x="FY", y="Attrition %", title="Attrition Trend")

    # 4. Gender Diversity (donut chart)
    gender_data = prepare_gender_data(filtered_df)
    render_donut_chart(gender_data, names="Gender", values="Count", title="Gender Diversity")

    # 5. Age Distribution (pie chart)
    age_data = prepare_age_distribution(filtered_df)
    render_pie_chart(age_data, names="Age Group", values="Count", title="Age Distribution")

    # 6. Tenure Distribution (pie chart)
    tenure_data = prepare_tenure_distribution(filtered_df)
    render_pie_chart(tenure_data, names="Tenure Group", values="Count", title="Tenure Distribution")

    # 7. Total Experience Distribution (bar chart)
    exp_data = prepare_experience_distribution(filtered_df)
    render_bar_chart(exp_data, x="Experience Group", y="Count", title="Total Experience Distribution")

    # 8. Transfer % Trend (line chart)
    transfer_data = prepare_transfer_trend(filtered_df)
    render_line_chart(transfer_data, x="FY", y="Transfer %", title="Transfer % Trend")

    # 9. Top Talent Ratio (pie chart)
    talent_data = prepare_top_talent_data(filtered_df)
    render_pie_chart(talent_data, names="Talent", values="Count", title="Top Talent Ratio")

    # 10. Performance Distribution (bell curve)
    perf_data = prepare_performance_distribution(filtered_df)
    render_bell_curve(perf_data, x="Rating", title="Performance Distribution")

    # 11. Education Type Distribution (donut chart)
    edu_data = prepare_education_distribution(filtered_df)
    render_donut_chart(edu_data, names="Qualification", values="Count", title="Education Type Distribution")

    # 12. Salary Distribution (box plot)
    salary_data = prepare_salary_distribution(filtered_df)
    render_box_plot(salary_data, y="CTC", title="Salary Distribution (CTC)")

def prepare_manpower_growth_data(df):
    # Your implementation here
    pass

def prepare_manpower_cost_data(df):
    pass

def prepare_attrition_data(df):
    pass

def prepare_gender_data(df):
    pass

def prepare_age_distribution(df):
    pass

def prepare_tenure_distribution(df):
    pass

def prepare_experience_distribution(df):
    pass

def prepare_transfer_trend(df):
    pass

def prepare_top_talent_data(df):
    pass

def prepare_performance_distribution(df):
    pass

def prepare_education_distribution(df):
    pass

def prepare_salary_distribution(df):
    pass

# Dummy renderer function placeholders

def render_line_chart(data, x, y, title):
    st.write(f"Line Chart: {title}")

def render_bar_chart(data, x, y, title):
    st.write(f"Bar Chart: {title}")

def render_pie_chart(data, names, values, title):
    st.write(f"Pie Chart: {title}")

def render_donut_chart(data, names, values, title):
    st.write(f"Donut Chart: {title}")

def render_box_plot(data, y, title):
    st.write(f"Box Plot: {title}")

def render_bell_curve(data, x, title):
    st.write(f"Bell Curve: {title}")

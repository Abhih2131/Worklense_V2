from datetime import datetime
import pandas as pd
import plotly.express as px

def get_last_fy_list(current_fy, n=5):
    return [f"FY-{str(current_fy-i)[-2:]}" for i in range(n-1, -1, -1)]

def prepare_manpower_growth_data(df, fy_list):
    # This function is only used to generate FY list for axis labeling.
    if 'date_of_joining' not in df.columns: return pd.DataFrame(columns=['FY','Headcount'])
    df = df.copy()
    df['FY'] = pd.to_datetime(df['date_of_joining'], errors='coerce').dt.year.apply(lambda y: f"FY-{str(y)[-2:]}" if pd.notnull(y) else None)
    grouped = df.groupby('FY').size().reset_index(name='Headcount')
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

def calc_kpis(df, fy_list, now):
    today = now
    current_fy = now.year + 1 if now.month >= 4 else now.year
    fy_start = datetime(current_fy-1, 4, 1)
    fy_end = datetime(current_fy, 3, 31)

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

    return [
        {"label": "Active Employees", "value": active, "type": "Integer"},
        {"label": f"Attrition Rate (FY {str(current_fy-1)[-2:]}-{str(current_fy)[-2:]})", "value": attrition, "type": "Percentage"},
        {"label": f"Joiners (FY {str(current_fy-1)[-2:]}-{str(current_fy)[-2:]})", "value": joiners, "type": "Integer"},
        {"label": "Total Cost (INR Cr)", "value": total_cost / 1e7, "type": "Currency"},
        {"label": "Diversity Ratio", "value": female_ratio, "type": "Percentage"},
        {"label": "Average Tenure", "value": avg_tenure, "type": "Years"},
        {"label": "Average Age", "value": avg_age, "type": "Years"},
        {"label": "Average Exp", "value": avg_total_exp, "type": "Years"},
    ]

def run_report(data, config):
    df = data.get("employee_master", pd.DataFrame())
    now = datetime.now()
    current_fy = now.year + 1 if now.month >= 4 else now.year
    fy_list = get_last_fy_list(current_fy, n=5)

    # --- Calculate KPIs first ---
    kpis = calc_kpis(df, fy_list, now)

    # --- Prepare chart data ---
    manpower_growth = prepare_manpower_growth_data(df, fy_list)
    attrition = prepare_attrition_data(df, fy_list)
    gender = prepare_gender_data(df)
    age = prepare_age_distribution(df)
    tenure = prepare_tenure_distribution(df)
    experience = prepare_experience_distribution(df)
    education = prepare_education_distribution(df)

    charts = []

    # --- Year-End Headcount Chart (Line) & Year-End Cost Chart (Bar) ---
    if not manpower_growth.empty:
        fy_years = [int(fy[-2:]) + 2000 for fy in manpower_growth["FY"]]
        fy_ends = [datetime(y, 3, 31) for y in fy_years]
        year_end_headcounts = []
        year_end_costs = []
        for i, fy_end in enumerate(fy_ends):
            if i == len(fy_ends) - 1:
                # YTD (as of today): match KPI
                headcount = df[
                    (pd.to_datetime(df["date_of_joining"], errors='coerce') <= now) &
                    (
                        df["date_of_exit"].isna() |
                        (pd.to_datetime(df["date_of_exit"], errors='coerce') > now)
                    )
                ].shape[0]
                cost = df[
                    (pd.to_datetime(df["date_of_joining"], errors='coerce') <= now) &
                    (
                        df["date_of_exit"].isna() |
                        (pd.to_datetime(df["date_of_exit"], errors='coerce') > now)
                    )
                ]["total_ctc_pa"].sum() if "total_ctc_pa" in df.columns else 0
            else:
                # Past FY: count as of March 31
                headcount = df[
                    (pd.to_datetime(df["date_of_joining"], errors='coerce') <= fy_end) &
                    (
                        df["date_of_exit"].isna() |
                        (pd.to_datetime(df["date_of_exit"], errors='coerce') > fy_end)
                    )
                ].shape[0]
                cost = df[
                    (pd.to_datetime(df["date_of_joining"], errors='coerce') <= fy_end) &
                    (
                        df["date_of_exit"].isna() |
                        (pd.to_datetime(df["date_of_exit"], errors='coerce') > fy_end)
                    )
                ]["total_ctc_pa"].sum() if "total_ctc_pa" in df.columns else 0
            year_end_headcounts.append(headcount)
            year_end_costs.append(cost / 1e7)
        manpower_growth["Year-End Headcount"] = year_end_headcounts
        manpower_growth["Year-End Cost (INR Cr)"] = year_end_costs
        manpower_growth["FY"] = manpower_growth["FY"].astype(str)
        if len(manpower_growth) > 0:
            manpower_growth.loc[manpower_growth.index[-1], "FY"] = "YTD"

        fig1 = px.line(
            manpower_growth,
            x="FY",
            y="Year-End Headcount",
            title="Year-End Headcount",
            text="Year-End Headcount"
        )
        fig1.update_traces(textposition="top center")
        fig1.update_yaxes(range=[0, max(manpower_growth["Year-End Headcount"]) * 1.2])
        charts.append(fig1)

        fig2 = px.bar(
            manpower_growth,
            x="FY",
            y="Year-End Cost (INR Cr)",
            title="Year-End Manpower Cost (INR Cr)",
            text_auto=True
        )
        fig2.update_yaxes(range=[0, max(manpower_growth["Year-End Cost (INR Cr)"]) * 1.2])
        charts.append(fig2)

    # --- All Other Charts Unchanged ---
    if not attrition.empty:
        charts.append(px.line(attrition, x="FY", y="Attrition %", title="Attrition Rate"))
    if not gender.empty:
        charts.append(px.pie(gender, names="Gender", values="Count", title="Gender Diversity"))
    if not age.empty:
        charts.append(px.bar(age, x="Age Group", y="Count", title="Age Distribution"))
    if not tenure.empty:
        charts.append(px.bar(tenure, x="Tenure Group", y="Count", title="Tenure Distribution"))
    if not experience.empty:
        charts.append(px.bar(experience, x="Experience Group", y="Count", title="Total Experience Distribution"))
    if not education.empty:
        charts.append(px.bar(education, x="Qualification", y="Count", title="Education Distribution"))

    return {
        "kpis": kpis,
        "charts": charts,
        "fy_list": fy_list,
        "as_of": now
    }

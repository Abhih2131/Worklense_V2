from datetime import datetime

def get_last_fy_list(current_fy, n=5):
    return [f"FY-{str(current_fy-i)[-2:]}" for i in range(n-1, -1, -1)]

# All prepare_xxx_data functions as before (copy from your previous code, unchanged):
# - prepare_manpower_growth_data
# - prepare_manpower_cost_data
# - prepare_attrition_data
# - prepare_gender_data
# - prepare_age_distribution
# - prepare_tenure_distribution
# - prepare_experience_distribution
# - prepare_education_distribution

def calc_kpis(df, fy_list, now):
    # Calculation logic for KPIs, as before (no rendering)
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
        {"label": f"Attrition Rate (Financial Year {str(current_fy-1)[-2:]}-{str(current_fy)[-2:]})", "value": attrition, "type": "Percentage"},
        {"label": f"Joiners (Financial Year {str(current_fy-1)[-2:]}-{str(current_fy)[-2:]})", "value": joiners, "type": "Integer"},
        {"label": "Total Cost (INR)", "value": total_cost, "type": "Currency"},
        {"label": "Female Ratio", "value": female_ratio, "type": "Percentage"},
        {"label": "Avg Tenure", "value": avg_tenure, "type": "Years"},
        {"label": "Avg Age", "value": avg_age, "type": "Years"},
        {"label": "Avg Total Exp", "value": avg_total_exp, "type": "Years"},
    ]

def run_report(data, config):
    import pandas as pd  # local import for safety
    df = data.get("employee_master", pd.DataFrame())
    now = datetime.now()
    current_fy = now.year + 1 if now.month >= 4 else now.year
    fy_list = get_last_fy_list(current_fy, n=5)

    result = {
        "kpis": calc_kpis(df, fy_list, now),
        "manpower_growth": prepare_manpower_growth_data(df, fy_list),
        "manpower_cost": prepare_manpower_cost_data(df, fy_list),
        "attrition": prepare_attrition_data(df, fy_list),
        "gender": prepare_gender_data(df),
        "age": prepare_age_distribution(df),
        "tenure": prepare_tenure_distribution(df),
        "experience": prepare_experience_distribution(df),
        "education": prepare_education_distribution(df),
        "fy_list": fy_list,
        "as_of": now
    }
    return result

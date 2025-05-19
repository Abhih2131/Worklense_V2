import pandas as pd

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
    df = df[df['date_of_exit'].isna()]  # Only active employees
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
    # Assuming a 'transfer_date' and 'transfer_flag' columns exist
    df = df.copy()
    if 'transfer_date' not in df.columns or 'transfer_flag' not in df.columns:
        return pd.DataFrame(columns=['FY', 'Transfer %'])
    df['FY'] = df['transfer_date'].dt.year.apply(lambda y: f"FY-{str(y)[-2:]}" if pd.notnull(y) else None)
    transfer_counts = df[df['transfer_flag'] == True].groupby('FY').size()
    total_counts = df.groupby('FY').size()
    transfer_percent = (transfer_counts / total_counts * 100).reset_index(name='Transfer %').fillna(0)
    return transfer_percent.sort_values('FY')

def prepare_top_talent_data(df):
    # Assuming 'is_top_talent' boolean column
    df = df.copy()
    if 'is_top_talent' not in df.columns:
        return pd.DataFrame({'Talent': ['Top Talent', 'Others'], 'Count': [0, len(df)]})
    counts = df['is_top_talent'].map({True: 'Top Talent', False: 'Others'}).value_counts().reset_index()
    counts.columns = ['Talent', 'Count']
    return counts

def prepare_performance_distribution(df):
    # Assuming 'performance_rating' column
    df = df.copy()
    if 'performance_rating' not in df.columns:
        return pd.DataFrame(columns=['Rating'])
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

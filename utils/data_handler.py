import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def load_all_data(data_files):
    data = {}
    for key, path in data_files.items():
        try:
            data[key] = pd.read_excel(path)
        except Exception:
            data[key] = pd.DataFrame()
    return data

def ensure_datetime(df, date_cols):
    for col in date_cols:
        if col in df:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

# utils/data_handler.py

import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def load_all_data(data_files):
    """
    Load all Excel data files into a dictionary of DataFrames.
    """
    data = {}
    for key, path in data_files.items():
        try:
            data[key] = pd.read_excel(path)
        except Exception:
            data[key] = pd.DataFrame()  # Empty fallback if missing/broken
    return data

def ensure_datetime(df, date_cols):
    """
    Convert listed columns in df to datetime (if present).
    """
    for col in date_cols:
        if col in df:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def filter_dataframe(df, filters):
    """
    Apply dict of {col: [values]} filters to df.
    If "All" or [] is selected for a column, skip filtering that column.
    """
    for col, selected in filters.items():
        if selected and ("All" not in selected):
            df = df[df[col].isin(selected)]
    return df

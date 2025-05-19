# utils/data_handler.py

import pandas as pd

def ensure_datetime(df, date_cols):
    """Converts given columns in DataFrame to datetime, in place."""
    for col in date_cols:
        if col in df:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def load_all_data(data_files):
    data = {}
    for key, path in data_files.items():
        try:
            data[key] = pd.read_excel(path)
        except Exception:
            data[key] = pd.DataFrame()  # Empty fallback
    return data

# utils/data_handler.py

import pandas as pd
import os

def load_all_data(data_files):
    data = {}
    for key, path in data_files.items():
        if os.path.exists(path):
            data[key] = pd.read_excel(path)
        else:
            data[key] = pd.DataFrame()  # Empty fallback
    return data

def load_config(config_file):
    if not os.path.exists(config_file):
        return {}
    xl = pd.ExcelFile(config_file)
    config = {sheet: xl.parse(sheet) for sheet in xl.sheet_names}
    return config

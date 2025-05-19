import streamlit as st
import pandas as pd
from datetime import datetime

FILTER_COLS = [
    "company", "business_unit", "department", "function",
    "zone", "area", "band", "employment_type"
]

# Utility functions for KPI calculations
def mean_age(series):
    now = datetime.now()
    ages = []
    for dob in pd.to_datetime(series.dropna(), errors='coerce'):
        ages.append((now - dob).days // 365)
    return sum(ages) / len(ages) if ages else 0

def run_report(data, config):
    st.title("Executive Summary")

    emp_df = data.get("employee_master", pd.DataFrame())
    filtered_df = emp_df.copy()

    # --- FILTER UI (hidden by default, show on button) ---
    show_filters = st.button("Show Filters")
    filter_values = {}

    if show_filters and not emp_df.empty:
        with st.expander("Filters", expanded=True):
            cols = st.columns(len(FILTER_COLS))
            for idx, col in enumerate(FILTER_COLS):
                unique_vals = ["All"] + sorted([str(x) for x in emp_df[col].dropna().unique()])
                selected = cols[idx].selectbox(col.replace("_", " ").title(), unique_vals)
                filter_values[col] = selected
                if selected != "All":
                    filtered_df = filtered_df[filtered_df[col] == selected]

    # --- Config-driven KPIs ---
    kpi_config = config.get("ExecutiveSummary_KPIs", pd.DataFrame())
    if not kpi_config.empty:
        # Sort by 'Order' if present
        if "Order" in kpi_config.columns:
            kpi_config = kpi_config.sort_values("Order")
        # Prepare values
        kpi_values = []
        for _, row in kpi_config.iterrows():
            formula = row["KPI_Formula/Field"]
            value = "--"
            try:
                if formula == "employment_status=='Active'":
                    value = (filtered_df['employment_status'] == 'Active').sum()
                elif formula == "employment_status=='Inactive'/count*100":
                    total = len(filtered_df)
                    inactive = (filtered_df['employment_status'] == 'Inactive').sum()
                    value = (inactive / total * 100) if total > 0 else 0
                elif formula == "sum(total_ctc_pa)":
                    value = filtered_df['total_ctc_pa'].sum()
                elif formula == "gender=='Female'/count*100":
                    total = len(filtered_df)
                    female = (filtered_df['gender'] == 'Female').sum()
                    value = (female / total * 100) if total > 0 else 0
                elif formula == "date_of_joining.year==current_year":
                    if "date_of_joining" in filtered_df:
                        this_year = datetime.now().year
                        value = filtered_df['date_of_joining'].apply(
                            lambda x: pd.to_datetime(x).year if pd.notnull(x) else None
                        ).eq(this_year).sum()
                    else:
                        value = 0
                elif formula == "mean(total_exp_yrs)":
                    value = filtered_df['total_exp_yrs'].mean() if "total_exp_yrs" in filtered_df else 0
                elif formula == "mean_age(date_of_birth)":
                    value = mean_age(filtered_df['date_of_birth']) if "date_of_birth" in filtered_df else 0
                else:
                    value = "--"
            except Exception as e:
                value = "--"
            kpi_values.append(value)

        # Display 4 per row
        display_labels = kpi_config["Display_Label"].tolist()
        display_units = kpi_config["Unit"].tolist() if "Unit" in kpi_config.columns else [""] * len(kpi_config)
        kpi_types = kpi_config["KPI_Type"].tolist()
        show_flags = kpi_config["Show_By_Default"].tolist()

        shown = 0
        for i in range(0, len(display_labels), 4):
            cols = st.columns(4)
            for j in range(4):
                idx = i + j
                if idx >= len(display_labels):
                    break
                if str(show_flags[idx]).upper() == "TRUE":
                    val = kpi_values[idx]
                    # Format as per type
                    if kpi_types[idx] == "Currency" and val != "--":
                        val = f"₹{val:,.0f}"
                    elif kpi_types[idx] == "Percentage" and val != "--":
                        val = f"{val:.1f}%"
                    elif kpi_types[idx] in ["Years", "Float"] and val != "--":
                        val = f"{val:.1f}"
                    elif kpi_types[idx] == "Integer" and val != "--":
                        val = f"{int(val):,}"
                    st.metric(label=display_labels[idx], value=val, help=f"Unit: {display_units[idx]}")
                    shown += 1
    else:
        st.info("No KPI config found for Executive Summary.")

    # --- Charts Placeholder ---
    st.subheader("Charts")
    chart_config = config.get("ExecutiveSummary_Charts", pd.DataFrame())
    if not chart_config.empty:
        for idx, row in chart_config.iterrows():
            st.write(f"**{row['Chart_Title']}**")
            st.write("Chart will go here.")
    else:
        st.info("No Chart config found for Executive Summary.")

    st.button("Export KPIs to Excel (Coming Soon)")

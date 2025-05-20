
import pandas as pd
import plotly.express as px
from datetime import datetime

def prepare_manpower_charts(df, fy_list, now):
    fy_years = [int(fy[-2:]) + 2000 for fy in fy_list]
    fy_ends = [datetime(y, 3, 31) for y in fy_years]
    year_end_headcounts = []
    year_end_costs = []

    for i, fy_end in enumerate(fy_ends):
        if i == len(fy_ends) - 1:
            mask = (pd.to_datetime(df["date_of_joining"], errors="coerce") <= now) & (
                df["date_of_exit"].isna() | (pd.to_datetime(df["date_of_exit"], errors="coerce") > now)
            )
        else:
            mask = (pd.to_datetime(df["date_of_joining"], errors="coerce") <= fy_end) & (
                df["date_of_exit"].isna() | (pd.to_datetime(df["date_of_exit"], errors="coerce") > fy_end)
            )

        headcount = df[mask].shape[0]
        cost = df.loc[mask, "total_ctc_pa"].sum() / 1e7 if "total_ctc_pa" in df.columns else 0

        year_end_headcounts.append(headcount)
        year_end_costs.append(cost)

    df_out = pd.DataFrame({
        "FY": fy_list,
        "Year-End Headcount": year_end_headcounts,
        "Year-End Cost (INR Cr)": year_end_costs
    })

    df_out.loc[df_out.index[-1], "FY"] = "Today"

    fig1 = px.line(
        df_out,
        x="FY",
        y="Year-End Headcount",
        title="Year-End Headcount",
        text="Year-End Headcount"
    )
    fig1.update_traces(textposition="top center")
    fig1.update_yaxes(range=[0, max(df_out["Year-End Headcount"]) * 1.2])

    fig2 = px.bar(
        df_out,
        x="FY",
        y="Year-End Cost (INR Cr)",
        title="Year-End Manpower Cost (INR Cr)",
        text="Year-End Cost (INR Cr)"
    )
    fig2.update_traces(textposition="outside")
    fig2.update_yaxes(range=[0, max(df_out["Year-End Cost (INR Cr)"]) * 1.2])

    return [fig1, fig2]

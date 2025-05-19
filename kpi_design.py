# kpi_design.py

KPI_STYLE = {
    "background_color": "#f6f8fa",
    "box_shadow": "0 2px 6px rgba(0,0,0,0.07)",
    "border_radius": "16px",
    "padding": "28px 6px",
    "box_width": 220,
    "box_height": 120,
    "font_size_label": "1.2rem",
    "font_size_value": "2.1rem",
    "value_color": "#21335b",
    "label_bold": True,
}

def format_kpi(value, kpi_type):
    if kpi_type == "Currency":
        value_in_cr = value / 1e7  # 1 Crore = 1e7
        return f"₹{value_in_cr:,.0f} Cr"
    elif kpi_type == "Percentage":
        return f"{value:.1f}%"
    elif kpi_type == "Years":
        return f"{value:.1f} Yrs"
    elif kpi_type == "Integer":
        return f"{int(value):,}"
    else:
        return str(value)

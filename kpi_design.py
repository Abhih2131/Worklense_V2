# kpi_design.py

# Central styling and formatter for all KPI cards

KPI_STYLE = {
    "box_width": 220,
    "box_height": 110,
    "background_color": "#f4f6fa",
    "font_size_label": "1rem",
    "font_size_value": "1.5rem",
    "label_bold": True,
    "value_color": "#0d47a1",
    "box_shadow": "0 2px 10px #e3e3e3",
    "border_radius": "18px",
    "padding": "18px"
}

def format_kpi(value, kpi_type):
    if value == "--":
        return value
    if kpi_type == "Currency":
        return f"₹{value:,.0f}"
    if kpi_type == "Percentage":
        return f"{value:.1f}%"
    if kpi_type in ("Years", "Float"):
        return f"{value:.1f}"
    if kpi_type == "Integer":
        return f"{int(value):,}"
    return str(value)

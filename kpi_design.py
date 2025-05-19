# kpi_design.py

KPI_STYLE = {
    "background_gradient": "linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%)",
    "accent_color": "#6366f1",
    "box_shadow": "0 6px 24px rgba(60, 72, 127, 0.10), 0 1.5px 4px rgba(99,102,241,0.07)",
    "border_radius": "20px",
    "padding": "26px 8px 18px 8px",
    "box_width": 240,
    "box_height": 125,
    "font_size_label": "1.14rem",
    "font_size_value": "2.45rem",
    "value_color": "#18181b",
    "label_color": "#6366f1",
    "label_bold": True,
    "accent_height": "5px",
    "accent_width": "60px",
    "accent_margin_bottom": "18px",
    "margin_bottom": "14px",
    "transition": "box-shadow 0.2s",
    "justify_content": "space-between",
    "align_items": "center",
}

def format_kpi(value, kpi_type):
    if kpi_type == "Currency":
        value_in_cr = value / 1e7
        return f"₹{value_in_cr:,.0f} Cr"
    elif kpi_type == "Percentage":
        return f"{value:.1f}%"
    elif kpi_type == "Years":
        return f"{value:.1f} Yrs"
    elif kpi_type == "Integer":
        return f"{int(value):,}"
    else:
        return str(value)

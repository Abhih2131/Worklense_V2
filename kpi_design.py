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
    "accent_border_radius": "8px",
    "margin_bottom": "14px",
    "transition": "box-shadow 0.2s",
    "justify_content": "space-between",
    "align_items": "center",
    "kpi_value_margin_top": "7px",
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

def render_kpi_card(label, value, kpi_type):
    # returns a single HTML string for the KPI card, fully styled via KPI_STYLE
    return f"""
        <div style="
            background:{KPI_STYLE['background_gradient']};
            box-shadow:{KPI_STYLE['box_shadow']};
            border-radius:{KPI_STYLE['border_radius']};
            padding:{KPI_STYLE['padding']};
            width:{KPI_STYLE['box_width']}px;
            height:{KPI_STYLE['box_height']}px;
            display:flex;
            flex-direction:column;
            justify-content:{KPI_STYLE['justify_content']};
            align-items:{KPI_STYLE['align_items']};
            margin-bottom:{KPI_STYLE['margin_bottom']};
            transition:{KPI_STYLE['transition']};">
            <div style="
                height:{KPI_STYLE['accent_height']};
                width:{KPI_STYLE['accent_width']};
                background:{KPI_STYLE['accent_color']};
                border-radius:{KPI_STYLE['accent_border_radius']};
                margin-bottom:{KPI_STYLE['accent_margin_bottom']};"></div>
            <span style="font-size:{KPI_STYLE['font_size_label']};
                         font-weight:{'bold' if KPI_STYLE['label_bold'] else 'normal'};
                         color:{KPI_STYLE['label_color']};">
                {label}
            </span>
            <span style="font-size:{KPI_STYLE['font_size_value']};
                         color:{KPI_STYLE['value_color']};
                         margin-top:{KPI_STYLE['kpi_value_margin_top']};">
                {format_kpi(value, kpi_type)}
            </span>
        </div>
    """

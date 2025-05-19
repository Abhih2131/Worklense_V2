
KPI_STYLE = {
    "background": "#F7F9FB",
    "border_radius": "18px",
    "box_shadow": "0 2px 12px rgba(80,120,160,0.10)",
    "padding": "22px 0 10px 0",
    "width": "100%",
    "height": "96px",
    "value_font_size": "2.0rem",
    "value_color": "#4359B8",
    "label_font_size": "1.08rem",
    "label_color": "#080808",
    "label_bold": True,
    "margin_bottom": "6px",
    "text_align": "center",
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
    return f"""
    <div style="
        background:{KPI_STYLE['background']};
        border-radius:{KPI_STYLE['border_radius']};
        box-shadow:{KPI_STYLE['box_shadow']};
        padding:{KPI_STYLE['padding']};
        width:{KPI_STYLE['width']};
        height:{KPI_STYLE['height']};
        margin-bottom:{KPI_STYLE['margin_bottom']};
        text-align:{KPI_STYLE['text_align']};
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
    ">
        <span style="
            font-size:{KPI_STYLE['value_font_size']};
            color:{KPI_STYLE['value_color']};
            font-weight:700;
        ">
            {format_kpi(value, kpi_type)}
        </span>
        <span style="
            font-size:{KPI_STYLE['label_font_size']};
            color:{KPI_STYLE['label_color']};
            font-weight:{'bold' if KPI_STYLE['label_bold'] else 'normal'};
            margin-top:4px;
        ">
            {label}
        </span>
    </div>
    """

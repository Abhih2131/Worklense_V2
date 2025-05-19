# kpi_design.py

KPI_STYLE = {
    # Soft gradients for up to 8 KPI cards
    "backgrounds": [
        "linear-gradient(135deg, #e0ecfc 0%, #f8f9fc 100%)",   # Blue
        "linear-gradient(135deg, #fceabb 0%, #f8f9fc 100%)",   # Yellow
        "linear-gradient(135deg, #fceabb 0%, #f7f7f7 100%)",   # Gold
        "linear-gradient(135deg, #e0fcf7 0%, #f8f9fc 100%)",   # Teal
        "linear-gradient(135deg, #ffe1e9 0%, #f8f9fc 100%)",   # Pink
        "linear-gradient(135deg, #dbeafe 0%, #f8f9fc 100%)",   # Light Blue
        "linear-gradient(135deg, #fee2f8 0%, #f8f9fc 100%)",   # Light Pink
        "linear-gradient(135deg, #f1f5f9 0%, #f8f9fc 100%)",   # Neutral
    ],
    "box_shadow": "0 2px 12px rgba(60,72,127,0.11)",
    "border_radius": "18px",
    "padding": "18px 12px",
    "box_width": 208,
    "box_height": 92,
    "font_size_label": "1.04rem",
    "font_size_value": "1.8rem",
    "value_color": "#111827",
    "label_color": "#6366f1",    # Indigo
    "label_bold": True,
    "accent_height": "4px",
    "accent_width": "44px",
    "accent_margin_bottom": "10px",
    "accent_border_radius": "4px",
    "margin_bottom": "10px",
    "transition": "box-shadow 0.12s",
    "justify_content": "space-between",
    "align_items": "center",
    "kpi_value_margin_top": "3px",
    # Accent colors for KPI label bar
    "accent_colors": [
        "#60a5fa", "#fbbf24", "#f59e42", "#34d399", "#f472b6", "#3b82f6", "#ec4899", "#64748b"
    ]
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

def render_kpi_card(label, value, kpi_type, idx):
    # idx for color selection
    background = KPI_STYLE['backgrounds'][idx % len(KPI_STYLE['backgrounds'])]
    accent = KPI_STYLE['accent_colors'][idx % len(KPI_STYLE['accent_colors'])]
    return f"""
        <div style="
            background:{background};
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
                background:{accent};
                border-radius:{KPI_STYLE['accent_border_radius']};
                margin-bottom:{KPI_STYLE['accent_margin_bottom']};"></div>
            <span style="font-size:{KPI_STYLE['font_size_label']};
                         font-weight:{'bold' if KPI_STYLE['label_bold'] else 'normal'};
                         color:{KPI_STYLE['label_color']}; letter-spacing: 0.2px;">
                {label}
            </span>
            <span style="font-size:{KPI_STYLE['font_size_value']};
                         color:{KPI_STYLE['value_color']};
                         margin-top:{KPI_STYLE['kpi_value_margin_top']};
                         font-weight: 500;">
                {format_kpi(value, kpi_type)}
            </span>
        </div>
    """

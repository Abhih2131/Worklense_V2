def render_kpi_card(label, value, value_type="Integer"):
    """
    Returns HTML for a modern, visually appealing KPI card.
    Supports type-based value formatting.
    """
    # Type-based formatting
    if value_type == "Currency":
        value_str = f"₹ {value:,.0f}"
    elif value_type == "Percentage":
        value_str = f"{value:,.1f}%"
    elif value_type == "Years":
        value_str = f"{value:,.1f} yrs"
    else:
        value_str = f"{value:,.0f}"

    return f"""
    <div class="kpi-card">
        <div class="kpi-accent"></div>
        <span class="kpi-label">{label}</span>
        <span class="kpi-value">{value_str}</span>
    </div>
    """

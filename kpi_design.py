# kpi_design.py

def render_kpi_card(label, value, value_type="Integer"):
    """
    Returns HTML for a KPI card. Supports type-based formatting.
    """
    # Type-based value formatting
    if value_type == "Currency":
        value_str = f"₹ {value:,.0f}"
    elif value_type == "Percentage":
        value_str = f"{value:,.1f}%"
    elif value_type == "Years":
        value_str = f"{value:,.1f} yrs"
    else:
        value_str = f"{value:,.0f}"

    # HTML for KPI card (customize as you like)
    return f"""
    <div style="
        background: #fff;
        border-radius: 16px;
        box-shadow: 0 1px 4px rgba(20,42,79,0.10);
        padding: 1.1rem 1.6rem 0.9rem 1.6rem;
        min-height: 80px;
        margin-bottom: 0.7rem;
        display: flex;
        flex-direction: column;
        align-items: flex-start;">
        <span style="font-size: 1.15rem; color: #8C98A4; font-weight: 600;">{label}</span>
        <span style="font-size: 2.1rem; font-weight: bold; color: #183153; margin-top: 0.35rem;">{value_str}</span>
    </div>
    """

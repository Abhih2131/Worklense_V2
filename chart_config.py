# chart_config.py

"""
Centralized configuration mapping HR metrics to allowed chart types
and their rendering function names.

This enables dynamic chart selection and modular extensibility.
"""

CHART_CONFIG = {
    "manpower_growth": {
        "description": "Workforce Size Over Time",
        "chart_types": ["line", "area", "animated_line"],
        "renderers": ["render_line_chart", "render_area_chart", "render_animated_line_chart"]
    },
    "manpower_cost": {
        "description": "Manpower Cost Trend",
        "chart_types": ["bar", "line", "stacked_bar"],
        "renderers": ["render_bar_chart", "render_line_chart", "render_stacked_bar_chart"]
    },
    "attrition": {
        "description": "Attrition Rate",
        "chart_types": ["line", "bar", "waterfall"],
        "renderers": ["render_line_chart", "render_bar_chart", "render_waterfall_chart"]
    },
    "gender_diversity": {
        "description": "Gender Diversity",
        "chart_types": ["donut", "pie", "icon_grid"],
        "renderers": ["render_donut_chart", "render_pie_chart", "render_icon_grid"]
    },
    "education_distribution": {
        "description": "Education Distribution",
        "chart_types": ["donut", "treemap", "horizontal_bar"],
        "renderers": ["render_donut_chart", "render_treemap", "render_horizontal_bar"]
    },
    "age_distribution": {
        "description": "Age Distribution",
        "chart_types": ["pie", "histogram", "box_plot"],
        "renderers": ["render_pie_chart", "render_histogram", "render_box_plot"]
    },
    "tenure_distribution": {
        "description": "Tenure Distribution",
        "chart_types": ["pie", "histogram", "violin_plot"],
        "renderers": ["render_pie_chart", "render_histogram", "render_violin_plot"]
    },
    "total_experience": {
        "description": "Total Experience Distribution",
        "chart_types": ["bar", "box_plot", "density_plot"],
        "renderers": ["render_bar_chart", "render_box_plot", "render_density_plot"]
    },
    "transfer_percent_trend": {
        "description": "Transfer % Trend",
        "chart_types": ["line", "step", "area"],
        "renderers": ["render_line_chart", "render_step_chart", "render_area_chart"]
    },
    "top_talent_ratio": {
        "description": "Top Talent Ratio",
        "chart_types": ["pie", "icon_grid", "kpi_card"],
        "renderers": ["render_pie_chart", "render_icon_grid", "render_kpi_card"]
    },
    "performance_distribution": {
        "description": "Performance Distribution",
        "chart_types": ["bell_curve", "histogram", "box_plot"],
        "renderers": ["render_bell_curve", "render_histogram", "render_box_plot"]
    },
    "salary_distribution": {
        "description": "Salary Distribution (CTC)",
        "chart_types": ["box_plot", "violin_plot", "histogram"],
        "renderers": ["render_box_plot", "render_violin_plot", "render_histogram"]
    }
}

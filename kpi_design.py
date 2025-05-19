with cols[j]:
    st.markdown(
        f"""
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
                {kpi['label']}
            </span>
            <span style="font-size:{KPI_STYLE['font_size_value']};
                         color:{KPI_STYLE['value_color']};
                         margin-top:{KPI_STYLE['kpi_value_margin_top']};">
                {format_kpi(kpi['value'], kpi['type'])}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

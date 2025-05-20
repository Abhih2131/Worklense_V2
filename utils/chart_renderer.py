import streamlit as st
import plotly.express as px
from utils.format_utils import indian_format, format_financial_year

def render_line_chart(df, x, y, title=None):
    template = st.session_state.get("plotly_template", "plotly")
    if df.empty or x not in df.columns or y not in df.columns:
        st.write("No Data")
        return

    df['label'] = df[y].apply(indian_format)
    df[x] = df[x].apply(format_financial_year)
    max_val = df[y].max()

    fig = px.line(df, x=x, y=y, markers=True, template=template, text='label', title=title)
    fig.update_traces(
        textposition="top center",
        textfont=dict(size=14),
        hovertemplate=f"<b>%{{x}}</b><br>{y}: %{{text}}"
    )
    fig.update_yaxes(
        range=[0, max_val * 1.2],
        tickformat=",",
        title=None
    )
    fig.update_layout(margin=dict(l=30, r=20, t=30, b=30))
    st.plotly_chart(fig, use_container_width=True)

def render_bar_chart(df, x, y, title=None):
    template = st.session_state.get("plotly_template", "plotly")
    if df.empty or x not in df.columns or y not in df.columns:
        st.write("No Data")
        return

    df['label'] = df[y].apply(indian_format)
    df[x] = df[x].apply(format_financial_year)
    max_val = df[y].max()

    fig = px.bar(df, x=x, y=y, template=template, text='label', title=title)
    fig.update_traces(
        textposition='outside',
        texttemplate='%{text}',
        hovertemplate=f"<b>%{{x}}</b><br>{y}: %{{text}}"
    )
    fig.update_yaxes(
        range=[0, max_val * 1.2],
        tickformat=",",
        title=None
    )
    fig.update_layout(margin=dict(l=30, r=20, t=30, b=30))
    st.plotly_chart(fig, use_container_width=True)

def render_pie_chart(df, names, values, title=None):
    template = st.session_state.get("plotly_template", "plotly")
    if df.empty or names not in df.columns or values not in df.columns:
        st.write("No Data")
        return

    df = df.sort_values(values, ascending=False)
    df['label'] = df[values].apply(indian_format)
    fig = px.pie(
        df,
        names=names,
        values=values,
        template=template,
        hole=0,
        category_orders={names: list(df[names])},
        title=title
    )
    fig.update_traces(
        textinfo='label+percent+value',
        textposition='outside',
        pull=[0.05] * len(df),
        showlegend=True
    )
    fig.update_layout(
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.0,
            font=dict(size=13),
            traceorder='normal'
        ),
        margin=dict(l=30, r=20, t=30, b=30)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_donut_chart(df, names, values, title=None):
    template = st.session_state.get("plotly_template", "plotly")
    if df.empty or names not in df.columns or values not in df.columns:
        st.write("No Data")
        return

    df = df.sort_values(values, ascending=False)
    df['label'] = df[values].apply(indian_format)
    fig = px.pie(
        df,
        names=names,
        values=values,
        template=template,
        hole=0.5,
        category_orders={names: list(df[names])},
        title=title
    )
    fig.update_traces(
        textinfo='label+percent+value',
        textposition='outside',
        pull=[0.05] * len(df),
        showlegend=True
    )
    fig.update_layout(
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.0,
            font=dict(size=13),
            traceorder='normal'
        ),
        margin=dict(l=30, r=20, t=30, b=30)
    )
    st.plotly_chart(fig, use_container_width=True)

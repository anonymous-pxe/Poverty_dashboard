"""
Metric card components for displaying KPIs.
Simplified to use Streamlit native components only.
"""

import streamlit as st
from typing import Optional


def render_metric_card(label: str,
                       value: any,
                       delta: Optional[any] = None,
                       delta_color: str = "normal",
                       help_text: Optional[str] = None):
    """
    Render a single metric card using Streamlit's native st.metric.
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional change/delta value
        delta_color: 'normal', 'inverse', or 'off'
        help_text: Optional help text
    """
    st.metric(
        label=label,
        value=value,
        delta=delta,
        delta_color=delta_color,
        help=help_text
    )


def render_kpi_cards(metrics: dict):
    """
    Render multiple KPI cards in columns using native Streamlit components.
    
    Args:
        metrics: Dictionary with metric definitions
    """
    num_metrics = len(metrics)
    cols = st.columns(num_metrics)
    
    for idx, (label, metric_data) in enumerate(metrics.items()):
        with cols[idx]:
            st.metric(
                label=label,
                value=metric_data.get('value', 'N/A'),
                delta=metric_data.get('delta'),
                delta_color=metric_data.get('delta_color', 'normal'),
                help=metric_data.get('help')
            )


def render_summary_metrics(df, value_col: str, group_col: Optional[str] = None):
    """
    Render summary metrics from a DataFrame.
    
    Args:
        df: DataFrame to summarize
        value_col: Column to calculate metrics for
        group_col: Optional grouping column
    """
    cols = st.columns(5 if group_col else 4)
    
    idx = 0
    if group_col:
        with cols[idx]:
            st.metric("Total Groups", df[group_col].nunique())
        idx += 1
    
    with cols[idx]:
        st.metric("Average", f"{df[value_col].mean():.2f}")
    with cols[idx + 1]:
        st.metric("Median", f"{df[value_col].median():.2f}")
    with cols[idx + 2]:
        st.metric("Min", f"{df[value_col].min():.2f}")
    with cols[idx + 3]:
        st.metric("Max", f"{df[value_col].max():.2f}")


def render_comparison_metrics(value1: float, value2: float, label1: str, label2: str):
    """
    Render comparison metrics between two values.
    
    Args:
        value1: First value
        value2: Second value
        label1: Label for first value
        label2: Label for second value
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label1, f"{value1:.2f}")
    
    with col2:
        st.metric(label2, f"{value2:.2f}")
    
    with col3:
        difference = value2 - value1
        pct_change = (difference / value1 * 100) if value1 != 0 else 0
        st.metric(
            label="Difference",
            value=f"{difference:.2f}",
            delta=f"{pct_change:.1f}%"
        )


def render_trend_metric(current_value: float,
                       previous_value: float,
                       label: str,
                       format_str: str = "{:.2f}"):
    """
    Render a metric with trend indicator.
    
    Args:
        current_value: Current period value
        previous_value: Previous period value
        label: Metric label
        format_str: Format string for values
    """
    change = current_value - previous_value
    pct_change = (change / previous_value * 100) if previous_value != 0 else 0
    
    st.metric(
        label=label,
        value=format_str.format(current_value),
        delta=f"{pct_change:+.1f}%",
        delta_color="inverse" if "poverty" in label.lower() or "unemployment" in label.lower() else "normal"
    )


def render_colored_metric(label: str,
                         value: any,
                         color: str = "blue",
                         icon: str = "📊"):
    """
    Render a metric with icon (legacy compatibility - now uses native metrics).
    
    Args:
        label: Metric label
        value: Metric value
        color: Color theme (ignored, uses Streamlit default)
        icon: Icon emoji
    """
    st.metric(f"{icon} {label}", value)

"""
Metric card components for displaying KPIs.
"""

import streamlit as st
from typing import Optional


def render_metric_card(label: str,
                       value: any,
                       delta: Optional[any] = None,
                       delta_color: str = "normal",
                       help_text: Optional[str] = None):
    """
    Render a single metric card.
    
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
    Render multiple KPI cards in columns.
    
    Args:
        metrics: Dictionary with metric definitions
                Example: {
                    'Total Countries': {'value': 100, 'delta': 5},
                    'Avg Poverty Rate': {'value': '15.3%', 'delta': '-2.1%', 'delta_color': 'inverse'}
                }
    """
    num_metrics = len(metrics)
    cols = st.columns(num_metrics)
    
    for idx, (label, metric_data) in enumerate(metrics.items()):
        with cols[idx]:
            render_metric_card(
                label=label,
                value=metric_data.get('value', 'N/A'),
                delta=metric_data.get('delta'),
                delta_color=metric_data.get('delta_color', 'normal'),
                help_text=metric_data.get('help')
            )


def render_summary_metrics(df, value_col: str, group_col: Optional[str] = None):
    """
    Render summary metrics from a DataFrame.
    
    Args:
        df: DataFrame to summarize
        value_col: Column to calculate metrics for
        group_col: Optional grouping column
    """
    metrics = {}
    
    if group_col:
        metrics['Total Groups'] = {
            'value': df[group_col].nunique(),
            'help': f'Number of unique {group_col}s'
        }
    
    metrics['Average'] = {
        'value': f"{df[value_col].mean():.2f}",
        'help': f'Mean {value_col}'
    }
    
    metrics['Median'] = {
        'value': f"{df[value_col].median():.2f}",
        'help': f'Median {value_col}'
    }
    
    metrics['Min'] = {
        'value': f"{df[value_col].min():.2f}",
        'help': f'Minimum {value_col}'
    }
    
    metrics['Max'] = {
        'value': f"{df[value_col].max():.2f}",
        'help': f'Maximum {value_col}'
    }
    
    render_kpi_cards(metrics)


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
        st.metric(label=label1, value=f"{value1:.2f}")
    
    with col2:
        st.metric(label=label2, value=f"{value2:.2f}")
    
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
    Render a colored metric card with custom styling.
    
    Args:
        label: Metric label
        value: Metric value
        color: Color theme (blue, green, red, orange)
        icon: Icon emoji
    """
    color_map = {
        'blue': '#1f77b4',
        'green': '#2ecc71',
        'red': '#e74c3c',
        'orange': '#f39c12',
        'purple': '#9b59b6'
    }
    
    bg_color = color_map.get(color, '#1f77b4')
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {bg_color}20 0%, {bg_color}40 100%);
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid {bg_color};
            margin: 10px 0;
        ">
            <h4 style="margin: 0; color: {bg_color};">{icon} {label}</h4>
            <h2 style="margin: 10px 0 0 0; color: #333;">{value}</h2>
        </div>
    """, unsafe_allow_html=True)

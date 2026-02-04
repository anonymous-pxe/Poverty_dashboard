"""
Metric card components for displaying KPIs.
Enhanced with beautiful modern UI/UX.
"""

import streamlit as st
from typing import Optional


def render_metric_card(label: str,
                       value: any,
                       delta: Optional[any] = None,
                       delta_color: str = "normal",
                       help_text: Optional[str] = None):
    """
    Render a single metric card with standard Streamlit styling.
    
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
    Render multiple KPI cards in columns with enhanced styling.
    
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
            render_enhanced_metric(
                label=label,
                value=metric_data.get('value', 'N/A'),
                delta=metric_data.get('delta'),
                icon=metric_data.get('icon', '📊'),
                color=metric_data.get('color', 'blue')
            )


def render_enhanced_metric(label: str,
                          value: any,
                          delta: Optional[any] = None,
                          icon: str = "📊",
                          color: str = "blue"):
    """
    Render an enhanced metric card with custom styling and icons.
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional delta value
        icon: Icon emoji
        color: Color theme (blue, green, red, orange, purple)
    """
    # Color mapping
    color_map = {
        'blue': {
            'gradient': 'linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%)',
            'bg': 'rgba(30, 136, 229, 0.08)',
            'text': '#1e88e5'
        },
        'green': {
            'gradient': 'linear-gradient(135deg, #66bb6a 0%, #43a047 100%)',
            'bg': 'rgba(102, 187, 106, 0.08)',
            'text': '#43a047'
        },
        'red': {
            'gradient': 'linear-gradient(135deg, #ef5350 0%, #d32f2f 100%)',
            'bg': 'rgba(239, 83, 80, 0.08)',
            'text': '#d32f2f'
        },
        'orange': {
            'gradient': 'linear-gradient(135deg, #ffa726 0%, #fb8c00 100%)',
            'bg': 'rgba(255, 167, 38, 0.08)',
            'text': '#fb8c00'
        },
        'purple': {
            'gradient': 'linear-gradient(135deg, #ab47bc 0%, #8e24aa 100%)',
            'bg': 'rgba(171, 71, 188, 0.08)',
            'text': '#8e24aa'
        },
        'teal': {
            'gradient': 'linear-gradient(135deg, #26a69a 0%, #00897b 100%)',
            'bg': 'rgba(38, 166, 154, 0.08)',
            'text': '#00897b'
        }
    }
    
    colors = color_map.get(color, color_map['blue'])
    
    # Delta formatting
    delta_html = ""
    if delta is not None:
        delta_str = str(delta)
        is_positive = not delta_str.startswith('-')
        delta_color = '#43a047' if is_positive else '#d32f2f'
        delta_icon = '↗' if is_positive else '↘'
        
        delta_html = f"""
        <div style="
            margin-top: 0.75rem;
            padding: 0.4rem 0.8rem;
            background: {'rgba(102, 187, 106, 0.1)' if is_positive else 'rgba(239, 83, 80, 0.1)'};
            border-radius: 6px;
            display: inline-block;
        ">
            <span style="color: {delta_color}; font-weight: 600; font-size: 0.875rem;">
                {delta_icon} {delta}
            </span>
        </div>
        """
    
    st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border: 2px solid transparent;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            margin-bottom: 1rem;
        " onmouseover="this.style.borderColor='{colors['text']}'; this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 24px rgba(0,0,0,0.15)'"
           onmouseout="this.style.borderColor='transparent'; this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'">
            
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 4px;
                background: {colors['gradient']};
            "></div>
            
            <div style="
                display: flex;
                align-items: center;
                margin-bottom: 0.75rem;
            ">
                <div style="
                    width: 48px;
                    height: 48px;
                    border-radius: 12px;
                    background: {colors['bg']};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.5rem;
                    margin-right: 0.75rem;
                ">
                    {icon}
                </div>
                <div style="flex: 1;">
                    <div style="
                        color: #546e7a;
                        font-size: 0.75rem;
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        margin-bottom: 0.25rem;
                    ">
                        {label}
                    </div>
                </div>
            </div>
            
            <div style="
                font-size: 2rem;
                font-weight: 700;
                color: {colors['text']};
                margin: 0.5rem 0;
            ">
                {value}
            </div>
            
            {delta_html}
        </div>
    """, unsafe_allow_html=True)


def render_summary_metrics(df, value_col: str, group_col: Optional[str] = None):
    """
    Render summary metrics from a DataFrame with enhanced styling.
    
    Args:
        df: DataFrame to summarize
        value_col: Column to calculate metrics for
        group_col: Optional grouping column
    """
    metrics = {}
    
    if group_col:
        metrics['Total Groups'] = {
            'value': df[group_col].nunique(),
            'icon': '🏷️',
            'color': 'purple',
            'help': f'Number of unique {group_col}s'
        }
    
    metrics['Average'] = {
        'value': f"{df[value_col].mean():.2f}",
        'icon': '📊',
        'color': 'blue',
        'help': f'Mean {value_col}'
    }
    
    metrics['Median'] = {
        'value': f"{df[value_col].median():.2f}",
        'icon': '📈',
        'color': 'teal',
        'help': f'Median {value_col}'
    }
    
    metrics['Min'] = {
        'value': f"{df[value_col].min():.2f}",
        'icon': '⬇️',
        'color': 'green',
        'help': f'Minimum {value_col}'
    }
    
    metrics['Max'] = {
        'value': f"{df[value_col].max():.2f}",
        'icon': '⬆️',
        'color': 'orange',
        'help': f'Maximum {value_col}'
    }
    
    render_kpi_cards(metrics)


def render_comparison_metrics(value1: float, value2: float, label1: str, label2: str):
    """
    Render comparison metrics between two values with visual styling.
    
    Args:
        value1: First value
        value2: Second value
        label1: Label for first value
        label2: Label for second value
    """
    col1, col2, col3 = st.columns(3)
    
    difference = value2 - value1
    pct_change = (difference / value1 * 100) if value1 != 0 else 0
    
    with col1:
        render_enhanced_metric(
            label=label1,
            value=f"{value1:.2f}",
            icon="📍",
            color="blue"
        )
    
    with col2:
        render_enhanced_metric(
            label=label2,
            value=f"{value2:.2f}",
            icon="📍",
            color="teal"
        )
    
    with col3:
        render_enhanced_metric(
            label="Difference",
            value=f"{difference:.2f}",
            delta=f"{pct_change:.1f}%",
            icon="📊",
            color="purple"
        )


def render_trend_metric(current_value: float,
                       previous_value: float,
                       label: str,
                       format_str: str = "{:.2f}",
                       icon: str = "📊"):
    """
    Render a metric with trend indicator and beautiful styling.
    
    Args:
        current_value: Current period value
        previous_value: Previous period value
        label: Metric label
        format_str: Format string for values
        icon: Icon emoji
    """
    change = current_value - previous_value
    pct_change = (change / previous_value * 100) if previous_value != 0 else 0
    
    # Determine color based on label context
    is_inverse = any(word in label.lower() for word in ['poverty', 'unemployment', 'gap'])
    color = 'green' if (change < 0 and is_inverse) or (change > 0 and not is_inverse) else 'red'
    
    render_enhanced_metric(
        label=label,
        value=format_str.format(current_value),
        delta=f"{pct_change:+.1f}%",
        icon=icon,
        color=color
    )


def render_colored_metric(label: str,
                         value: any,
                         color: str = "blue",
                         icon: str = "📊"):
    """
    Render a colored metric card with custom styling (legacy compatibility).
    
    Args:
        label: Metric label
        value: Metric value
        color: Color theme
        icon: Icon emoji
    """
    render_enhanced_metric(label=label, value=value, color=color, icon=icon)


def render_hero_metrics(metrics: list):
    """
    Render large hero-style metrics for important KPIs.
    
    Args:
        metrics: List of dicts with 'label', 'value', 'icon', 'color'
    """
    cols = st.columns(len(metrics))
    
    for idx, metric in enumerate(metrics):
        with cols[idx]:
            color_map = {
                'blue': '#1e88e5',
                'green': '#43a047',
                'red': '#d32f2f',
                'orange': '#fb8c00',
                'purple': '#8e24aa',
                'teal': '#00897b'
            }
            
            color_code = color_map.get(metric.get('color', 'blue'), '#1e88e5')
            
            st.markdown(f"""
                <div style="
                    background: white;
                    padding: 2rem;
                    border-radius: 20px;
                    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
                    text-align: center;
                    border: 2px solid transparent;
                    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                " onmouseover="this.style.borderColor='{color_code}'; this.style.transform='scale(1.05)'"
                   onmouseout="this.style.borderColor='transparent'; this.style.transform='scale(1)'">
                    
                    <div style="
                        width: 64px;
                        height: 64px;
                        margin: 0 auto 1rem;
                        border-radius: 16px;
                        background: linear-gradient(135deg, {color_code}15 0%, {color_code}30 100%);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 2rem;
                    ">
                        {metric.get('icon', '📊')}
                    </div>
                    
                    <div style="
                        color: #546e7a;
                        font-size: 0.875rem;
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 1px;
                        margin-bottom: 0.75rem;
                    ">
                        {metric['label']}
                    </div>
                    
                    <div style="
                        font-size: 2.5rem;
                        font-weight: 700;
                        color: {color_code};
                        line-height: 1;
                    ">
                        {metric['value']}
                    </div>
                </div>
            """, unsafe_allow_html=True)


def render_stat_card(title: str, 
                    value: str, 
                    subtitle: str = "",
                    icon: str = "📊",
                    color: str = "blue"):
    """
    Render a statistical card with icon and subtitle.
    
    Args:
        title: Card title
        value: Main value to display
        subtitle: Optional subtitle
        icon: Icon emoji
        color: Color theme
    """
    color_map = {
        'blue': '#1e88e5',
        'green': '#43a047',
        'red': '#d32f2f',
        'orange': '#fb8c00',
        'purple': '#8e24aa',
        'teal': '#00897b'
    }
    
    main_color = color_map.get(color, '#1e88e5')
    
    st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-left: 5px solid {main_color};
            margin: 1rem 0;
            transition: all 0.3s;
        " onmouseover="this.style.transform='translateX(5px)'; this.style.boxShadow='0 6px 16px rgba(0,0,0,0.15)'"
           onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'">
            
            <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                <span style="font-size: 1.5rem; margin-right: 0.75rem;">{icon}</span>
                <span style="color: #546e7a; font-weight: 600; font-size: 0.875rem;">
                    {title}
                </span>
            </div>
            
            <div style="font-size: 2rem; font-weight: 700; color: {main_color}; margin-bottom: 0.25rem;">
                {value}
            </div>
            
            {f'<div style="color: #78909c; font-size: 0.875rem;">{subtitle}</div>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)


def render_progress_metric(label: str,
                          current: float,
                          target: float,
                          unit: str = "%",
                          icon: str = "🎯"):
    """
    Render a metric with progress bar.
    
    Args:
        label: Metric label
        current: Current value
        target: Target value
        unit: Unit of measurement
        icon: Icon emoji
    """
    progress = min((current / target * 100) if target > 0 else 0, 100)
    
    st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin: 1rem 0;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div>
                    <span style="font-size: 1.25rem; margin-right: 0.5rem;">{icon}</span>
                    <span style="color: #546e7a; font-weight: 600;">{label}</span>
                </div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1e88e5;">
                    {current}{unit}
                </div>
            </div>
            
            <div style="
                width: 100%;
                height: 8px;
                background: #e0e0e0;
                border-radius: 10px;
                overflow: hidden;
                margin-bottom: 0.5rem;
            ">
                <div style="
                    width: {progress}%;
                    height: 100%;
                    background: linear-gradient(90deg, #42a5f5 0%, #1e88e5 100%);
                    border-radius: 10px;
                    transition: width 0.5s ease;
                "></div>
            </div>
            
            <div style="color: #78909c; font-size: 0.75rem; text-align: right;">
                Target: {target}{unit} ({progress:.1f}% achieved)
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_mini_metric(label: str, value: str, color: str = "blue"):
    """
    Render a compact metric for dense displays.
    
    Args:
        label: Metric label
        value: Metric value
        color: Color theme
    """
    color_map = {
        'blue': '#1e88e5',
        'green': '#43a047',
        'red': '#d32f2f',
        'orange': '#fb8c00'
    }
    
    main_color = color_map.get(color, '#1e88e5')
    
    st.markdown(f"""
        <div style="
            background: rgba(30, 136, 229, 0.05);
            padding: 0.75rem 1rem;
            border-radius: 8px;
            border-left: 3px solid {main_color};
            margin: 0.5rem 0;
        ">
            <div style="color: #546e7a; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.25rem;">
                {label}
            </div>
            <div style="color: {main_color}; font-size: 1.25rem; font-weight: 700;">
                {value}
            </div>
        </div>
    """, unsafe_allow_html=True)

"""
Dashboard page - Overview with KPIs and highlights.
"""

import streamlit as st
import pandas as pd
from data.data_loader import load_india_data, load_global_data, get_latest_year_data
from components.tables import render_top_bottom_table
from utils.visualization import create_line_chart, create_bar_chart
import config


def render_dashboard_page():
    """Render the main dashboard overview page."""
    st.title("📊 Poverty Dashboard Overview")
    st.markdown("### Key Performance Indicators & Highlights")
    
    # Load data
    try:
        india_data = load_india_data(area_type='Total', start_year=2010, end_year=2023)
        global_data = load_global_data(
            indicator='SI.POV.DDAY',
            country_codes=['IND', 'CHN', 'BRA', 'ZAF'],
            start_year=2010,
            end_year=2023
        )
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    # Get latest year data
    latest_india = get_latest_year_data(india_data)
    latest_global = get_latest_year_data(global_data)
    
    # Calculate KPIs
    st.markdown("---")
    st.subheader("🔑 Key Metrics - India")
    
    # India KPIs
    avg_poverty = latest_india['poverty_rate'].mean()
    avg_literacy = latest_india['literacy_rate'].mean()
    avg_unemployment = latest_india['unemployment_rate'].mean()
    total_states = latest_india['state'].nunique()
    
    # Historical comparison
    if len(india_data) > 0:
        oldest_year = india_data['year'].min()
        oldest_data = india_data[india_data['year'] == oldest_year]
        old_poverty = oldest_data['poverty_rate'].mean()
        poverty_change = avg_poverty - old_poverty
    else:
        poverty_change = 0
    
    # Use native Streamlit metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Avg Poverty Rate",
            value=f"{avg_poverty:.2f}%",
            delta=f"{poverty_change:.2f}%",
            delta_color='inverse',
            help='Average poverty rate across all states'
        )
    
    with col2:
        st.metric(
            label="Avg Literacy Rate",
            value=f"{avg_literacy:.2f}%",
            help='Average literacy rate across all states'
        )
    
    with col3:
        st.metric(
            label="Avg Unemployment",
            value=f"{avg_unemployment:.2f}%",
            delta_color='inverse',
            help='Average unemployment rate across all states'
        )
    
    with col4:
        st.metric(
            label="Total States",
            value=total_states,
            help='Number of states in the dataset'
        )
    
    # Global KPIs
    st.markdown("---")
    st.subheader("🌍 Global Poverty Indicators")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="🌐 Countries Tracked",
            value=latest_global['country'].nunique()
        )
    
    with col2:
        st.metric(
            label="📊 Avg Global Poverty Rate",
            value=f"{latest_global['value'].mean():.2f}%"
        )
    
    # Trends Section
    st.markdown("---")
    st.subheader("📈 Recent Trends")
    
    tab1, tab2 = st.tabs(["India Trends", "Global Trends"])
    
    with tab1:
        # India poverty trend
        recent_india = india_data[india_data['year'] >= 2015]
        yearly_avg = recent_india.groupby('year')['poverty_rate'].mean().reset_index()
        
        fig = create_line_chart(
            df=yearly_avg,
            x_col='year',
            y_col='poverty_rate',
            title='India Average Poverty Rate Trend (2015-2023)',
            x_label='Year',
            y_label='Poverty Rate (%)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Global poverty trend
        fig = create_line_chart(
            df=global_data,
            x_col='year',
            y_col='value',
            color_col='country',
            title='Global Poverty Trends - Selected Countries',
            x_label='Year',
            y_label='Poverty Rate (%)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top & Bottom Performers
    st.markdown("---")
    st.subheader("🏆 State Performance Analysis")
    
    render_top_bottom_table(
        df=latest_india,
        value_col='poverty_rate',
        label_col='state',
        n=5
    )
    
    # Recent Highlights
    st.markdown("---")
    st.subheader("💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Lowest Poverty State:** {latest_india.loc[latest_india['poverty_rate'].idxmin(), 'state']} 
        ({latest_india['poverty_rate'].min():.2f}%)
        """)
        
        st.success(f"""
        **Highest Literacy State:** {latest_india.loc[latest_india['literacy_rate'].idxmax(), 'state']} 
        ({latest_india['literacy_rate'].max():.2f}%)
        """)
    
    with col2:
        st.warning(f"""
        **Highest Poverty State:** {latest_india.loc[latest_india['poverty_rate'].idxmax(), 'state']} 
        ({latest_india['poverty_rate'].max():.2f}%)
        """)
        
        st.error(f"""
        **Highest Unemployment State:** {latest_india.loc[latest_india['unemployment_rate'].idxmax(), 'state']} 
        ({latest_india['unemployment_rate'].max():.2f}%)
        """)
    
    # Summary Statistics
    st.markdown("---")
    st.subheader("📋 Summary Statistics")
    
    summary_stats = latest_india[['poverty_rate', 'literacy_rate', 'unemployment_rate', 'per_capita_income']].describe()
    st.dataframe(summary_stats.T.round(2), use_container_width=True)

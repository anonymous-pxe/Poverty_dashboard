"""
Visualization page - Interactive charts and maps.
"""

import streamlit as st
from data.data_loader import load_india_data, load_global_data
from components.filters import render_filters
from utils.visualization import (
    create_line_chart,
    create_bar_chart,
    create_box_plot,
    create_pie_chart,
    create_scatter_plot,
    create_area_chart,
    create_histogram
)
import config


def render_visualization_page():
    """Render the data visualization page."""
    st.title("📉 Data Visualization")
    st.markdown("### Interactive charts and visual analysis")
    
    # Data source selection
    data_source = st.radio(
        "Select Data Source",
        options=["India State Data", "Global Data"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if data_source == "India State Data":
        render_india_visualizations()
    else:
        render_global_visualizations()


def render_india_visualizations():
    """Render India-specific visualizations."""
    st.subheader("🇮🇳 India State-wise Visualizations")
    
    # Filters
    filters = render_filters(
        show_year=True,
        show_state=True,
        show_country=False,
        show_area=True,
        show_indicator=False
    )
    
    year_range = filters.get('year_range', (2010, 2023))
    states = filters.get('states', config.INDIAN_STATES[:5])
    area_type = filters.get('area_type', 'Total')
    
    if not states:
        st.warning("Please select at least one state.")
        return
    
    # Load data
    try:
        with st.spinner("Loading data..."):
            data = load_india_data(
                states=states,
                area_type=area_type,
                start_year=year_range[0],
                end_year=year_range[1]
            )
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    # Chart type selection
    chart_type = st.selectbox(
        "Select Chart Type",
        options=[
            "Line Chart",
            "Bar Chart",
            "Area Chart",
            "Box Plot",
            "Scatter Plot",
            "Histogram"
        ]
    )
    
    # Variable selection
    col1, col2 = st.columns(2)
    
    with col1:
        x_var = st.selectbox(
            "X-Axis Variable",
            options=['year', 'state'],
            index=0
        )
    
    with col2:
        y_var = st.selectbox(
            "Y-Axis Variable",
            options=['poverty_rate', 'literacy_rate', 'unemployment_rate', 
                    'per_capita_income', 'mpi'],
            format_func=lambda x: x.replace('_', ' ').title()
        )
    
    st.markdown("---")
    
    # Generate visualization based on selection
    if chart_type == "Line Chart":
        fig = create_line_chart(
            df=data,
            x_col=x_var,
            y_col=y_var,
            color_col='state' if x_var != 'state' else None,
            title=f'{y_var.replace("_", " ").title()} by {x_var.title()}',
            x_label=x_var.title(),
            y_label=y_var.replace('_', ' ').title()
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Bar Chart":
        # For bar charts, use latest year if x is state
        if x_var == 'state':
            latest_year = data['year'].max()
            plot_data = data[data['year'] == latest_year]
        else:
            plot_data = data
        
        fig = create_bar_chart(
            df=plot_data,
            x_col=x_var,
            y_col=y_var,
            color_col='state' if x_var != 'state' else None,
            title=f'{y_var.replace("_", " ").title()} by {x_var.title()}'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Area Chart":
        fig = create_area_chart(
            df=data,
            x_col=x_var,
            y_col=y_var,
            color_col='state' if x_var != 'state' else None,
            title=f'{y_var.replace("_", " ").title()} Area Chart'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Box Plot":
        fig = create_box_plot(
            df=data,
            x_col='state' if len(states) > 1 else None,
            y_col=y_var,
            title=f'{y_var.replace("_", " ").title()} Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Scatter Plot":
        x_scatter = st.selectbox(
            "X-Axis for Scatter",
            options=['poverty_rate', 'literacy_rate', 'unemployment_rate', 
                    'per_capita_income'],
            format_func=lambda x: x.replace('_', ' ').title()
        )
        y_scatter = st.selectbox(
            "Y-Axis for Scatter",
            options=['poverty_rate', 'literacy_rate', 'unemployment_rate', 
                    'per_capita_income'],
            index=1,
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        fig = create_scatter_plot(
            df=data,
            x_col=x_scatter,
            y_col=y_scatter,
            color_col='state',
            title=f'{y_scatter.replace("_", " ").title()} vs {x_scatter.replace("_", " ").title()}',
            trendline='ols'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Histogram":
        fig = create_histogram(
            df=data,
            x_col=y_var,
            color_col='state' if len(states) > 1 else None,
            title=f'{y_var.replace("_", " ").title()} Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)


def render_global_visualizations():
    """Render global visualizations."""
    st.subheader("🌍 Global Visualizations")
    
    # Filters
    filters = render_filters(
        show_year=True,
        show_state=False,
        show_country=True,
        show_area=False,
        show_indicator=True
    )
    
    year_range = filters.get('year_range', (2010, 2023))
    countries = filters.get('countries', ['IND', 'CHN', 'BRA', 'ZAF'])
    indicator = filters.get('indicator', 'SI.POV.DDAY')
    
    if not countries:
        st.warning("Please select at least one country.")
        return
    
    # Load data
    try:
        with st.spinner("Loading global data..."):
            data = load_global_data(
                indicator=indicator,
                country_codes=countries,
                start_year=year_range[0],
                end_year=year_range[1]
            )
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    # Chart type selection
    chart_type = st.selectbox(
        "Select Chart Type",
        options=[
            "Line Chart",
            "Bar Chart",
            "Area Chart",
            "Box Plot"
        ]
    )
    
    st.markdown("---")
    
    # Generate visualization
    if chart_type == "Line Chart":
        fig = create_line_chart(
            df=data,
            x_col='year',
            y_col='value',
            color_col='country',
            title=f'{config.GLOBAL_INDICATORS[indicator]} Over Time',
            x_label='Year',
            y_label='Value'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Bar Chart":
        latest_year = data['year'].max()
        latest_data = data[data['year'] == latest_year]
        
        fig = create_bar_chart(
            df=latest_data,
            x_col='country',
            y_col='value',
            title=f'{config.GLOBAL_INDICATORS[indicator]} by Country ({latest_year})'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Area Chart":
        fig = create_area_chart(
            df=data,
            x_col='year',
            y_col='value',
            color_col='country',
            title=f'{config.GLOBAL_INDICATORS[indicator]} Area Chart'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Box Plot":
        fig = create_box_plot(
            df=data,
            x_col='country',
            y_col='value',
            title=f'{config.GLOBAL_INDICATORS[indicator]} Distribution by Country'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional insights
    st.markdown("---")
    st.subheader("📊 Quick Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Countries", data['country'].nunique())
    with col2:
        st.metric("Years", data['year'].nunique())
    with col3:
        st.metric("Avg Value", f"{data['value'].mean():.2f}")
    with col4:
        st.metric("Data Points", len(data))

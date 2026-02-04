"""
Filter components for data selection.
"""

import streamlit as st
from typing import List, Optional, Tuple
import config


def render_filters(show_year: bool = True,
                  show_state: bool = True,
                  show_country: bool = False,
                  show_area: bool = True,
                  show_indicator: bool = False) -> dict:
    """
    Render filter controls based on specified options.
    
    Args:
        show_year: Show year range selector
        show_state: Show state multi-select
        show_country: Show country multi-select
        show_area: Show area type selector
        show_indicator: Show indicator selector
    
    Returns:
        dict: Dictionary with selected filter values
    """
    filters = {}
    
    st.subheader("🔍 Filters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if show_year:
            year_range = st.slider(
                "Select Year Range",
                min_value=config.START_YEAR,
                max_value=config.END_YEAR,
                value=(2010, config.END_YEAR),
                key="year_filter"
            )
            filters['year_range'] = year_range
        
        if show_state:
            selected_states = st.multiselect(
                "Select States",
                options=config.INDIAN_STATES,
                default=config.INDIAN_STATES[:5],
                key="state_filter"
            )
            filters['states'] = selected_states
    
    with col2:
        if show_area:
            area_type = st.selectbox(
                "Select Area Type",
                options=config.AREA_TYPES,
                key="area_filter"
            )
            filters['area_type'] = area_type
        
        if show_country:
            from data.data_loader import load_countries_metadata
            countries_df = load_countries_metadata()
            
            selected_countries = st.multiselect(
                "Select Countries",
                options=countries_df['country_code'].tolist(),
                default=countries_df['country_code'].head(5).tolist(),
                format_func=lambda x: countries_df[countries_df['country_code'] == x]['country_name'].iloc[0],
                key="country_filter"
            )
            filters['countries'] = selected_countries
    
    if show_indicator:
        if show_country:
            # Global indicators
            indicator = st.selectbox(
                "Select Indicator",
                options=list(config.GLOBAL_INDICATORS.keys()),
                format_func=lambda x: config.GLOBAL_INDICATORS[x],
                key="indicator_filter"
            )
            filters['indicator'] = indicator
        else:
            # India indicators
            indicator = st.selectbox(
                "Select Indicator",
                options=config.INDIA_INDICATORS,
                key="india_indicator_filter"
            )
            filters['indicator'] = indicator
    
    return filters


def render_year_selector(label: str = "Select Year",
                        min_year: Optional[int] = None,
                        max_year: Optional[int] = None,
                        default_year: Optional[int] = None) -> int:
    """
    Render a single year selector.
    
    Args:
        label: Label for the selector
        min_year: Minimum year
        max_year: Maximum year
        default_year: Default selected year
    
    Returns:
        int: Selected year
    """
    if min_year is None:
        min_year = config.START_YEAR
    if max_year is None:
        max_year = config.END_YEAR
    if default_year is None:
        default_year = max_year
    
    year = st.selectbox(
        label,
        options=list(range(max_year, min_year - 1, -1)),
        index=0
    )
    
    return year


def render_comparison_filters() -> Tuple[List[str], int]:
    """
    Render filters for comparison views.
    
    Returns:
        tuple: (selected_items, selected_year)
    """
    col1, col2 = st.columns(2)
    
    with col1:
        items = st.multiselect(
            "Select Items to Compare",
            options=config.INDIAN_STATES,
            default=config.INDIAN_STATES[:3]
        )
    
    with col2:
        year = render_year_selector("Select Year for Comparison")
    
    return items, year


def render_date_range_filter(label: str = "Select Date Range") -> Tuple[int, int]:
    """
    Render a date range filter.
    
    Args:
        label: Label for the filter
    
    Returns:
        tuple: (start_year, end_year)
    """
    col1, col2 = st.columns(2)
    
    with col1:
        start_year = st.selectbox(
            "From Year",
            options=list(range(config.START_YEAR, config.END_YEAR + 1)),
            index=0
        )
    
    with col2:
        end_year = st.selectbox(
            "To Year",
            options=list(range(config.START_YEAR, config.END_YEAR + 1)),
            index=len(list(range(config.START_YEAR, config.END_YEAR + 1))) - 1
        )
    
    if start_year > end_year:
        st.warning("Start year cannot be greater than end year. Please adjust your selection.")
    
    return start_year, end_year

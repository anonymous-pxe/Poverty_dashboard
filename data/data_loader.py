"""
Unified data loader with caching for the Poverty Dashboard.
Handles data fetching and caching using Streamlit's cache_data decorator.
"""

import streamlit as st
import pandas as pd
from typing import Optional, List
import config
from .wb_api import fetch_world_bank_data, get_available_countries, fetch_multiple_indicators
from .india_poverty_api import (
    fetch_india_poverty_data, 
    get_india_states,
    fetch_india_rural_urban_comparison
)


@st.cache_data(ttl=config.CACHE_TTL)
def load_global_data(indicator: str, 
                     country_codes: Optional[List[str]] = None,
                     start_year: Optional[int] = None,
                     end_year: Optional[int] = None) -> pd.DataFrame:
    """
    Load global poverty data with caching.
    
    Args:
        indicator: World Bank indicator code
        country_codes: List of ISO country codes
        start_year: Starting year
        end_year: Ending year
    
    Returns:
        pd.DataFrame: Cached global poverty data
    """
    return fetch_world_bank_data(
        indicator=indicator,
        country_codes=country_codes,
        start_year=start_year,
        end_year=end_year
    )


@st.cache_data(ttl=config.CACHE_TTL)
def load_multiple_global_indicators(indicators: List[str],
                                   country_codes: Optional[List[str]] = None,
                                   start_year: Optional[int] = None,
                                   end_year: Optional[int] = None) -> dict:
    """
    Load multiple global indicators with caching.
    
    Args:
        indicators: List of indicator codes
        country_codes: List of country codes
        start_year: Start year
        end_year: End year
    
    Returns:
        dict: Dictionary with indicator codes as keys
    """
    return fetch_multiple_indicators(
        indicators=indicators,
        country_codes=country_codes,
        start_year=start_year,
        end_year=end_year
    )


@st.cache_data(ttl=config.CACHE_TTL)
def load_india_data(states: Optional[List[str]] = None,
                   area_type: str = 'Total',
                   start_year: Optional[int] = None,
                   end_year: Optional[int] = None) -> pd.DataFrame:
    """
    Load India state-wise poverty data with caching.
    
    Args:
        states: List of state names
        area_type: 'Rural', 'Urban', or 'Total'
        start_year: Starting year
        end_year: Ending year
    
    Returns:
        pd.DataFrame: Cached India poverty data
    """
    return fetch_india_poverty_data(
        states=states,
        area_type=area_type,
        start_year=start_year,
        end_year=end_year
    )


@st.cache_data(ttl=config.CACHE_TTL)
def load_rural_urban_comparison(states: Optional[List[str]] = None,
                               year: Optional[int] = None) -> pd.DataFrame:
    """
    Load rural vs urban comparison data with caching.
    
    Args:
        states: List of state names
        year: Specific year for comparison
    
    Returns:
        pd.DataFrame: Rural vs Urban comparison data
    """
    return fetch_india_rural_urban_comparison(states=states, year=year)


@st.cache_data(ttl=config.CACHE_TTL)
def load_countries_metadata() -> pd.DataFrame:
    """
    Load countries metadata with caching.
    
    Returns:
        pd.DataFrame: Countries metadata
    """
    return get_available_countries()


@st.cache_data(ttl=config.CACHE_TTL)
def load_states_metadata() -> pd.DataFrame:
    """
    Load Indian states metadata with caching.
    
    Returns:
        pd.DataFrame: States metadata
    """
    return get_india_states()


def load_all_area_types(states: Optional[List[str]] = None,
                       start_year: Optional[int] = None,
                       end_year: Optional[int] = None) -> pd.DataFrame:
    """
    Load data for all area types (Rural, Urban, Total) and combine.
    
    Args:
        states: List of state names
        start_year: Starting year
        end_year: Ending year
    
    Returns:
        pd.DataFrame: Combined data for all area types
    """
    dfs = []
    for area_type in config.AREA_TYPES:
        df = load_india_data(
            states=states,
            area_type=area_type,
            start_year=start_year,
            end_year=end_year
        )
        dfs.append(df)
    
    return pd.concat(dfs, ignore_index=True)


def get_latest_year_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get data for the most recent year available.
    
    Args:
        df: DataFrame with 'year' column
    
    Returns:
        pd.DataFrame: Data filtered for the latest year
    """
    latest_year = df['year'].max()
    return df[df['year'] == latest_year].copy()


def get_year_range(df: pd.DataFrame) -> tuple:
    """
    Get the year range from a DataFrame.
    
    Args:
        df: DataFrame with 'year' column
    
    Returns:
        tuple: (min_year, max_year)
    """
    return int(df['year'].min()), int(df['year'].max())

"""
Data module for the Poverty Dashboard.
Handles data fetching, caching, and preprocessing.
"""

from .wb_api import fetch_world_bank_data, get_available_countries
from .india_poverty_api import fetch_india_poverty_data, get_india_states
from .data_loader import load_global_data, load_india_data
from .preprocess import preprocess_data, filter_data, aggregate_data

__all__ = [
    'fetch_world_bank_data',
    'get_available_countries',
    'fetch_india_poverty_data',
    'get_india_states',
    'load_global_data',
    'load_india_data',
    'preprocess_data',
    'filter_data',
    'aggregate_data'
]

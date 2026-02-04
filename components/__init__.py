"""
UI Components module for the Poverty Dashboard.
Provides reusable UI components like sidebar, filters, metrics, and tables.
"""

from .sidebar import render_sidebar
from .filters import render_filters
from .metrics import render_kpi_cards, render_metric_card
from .tables import render_styled_table, render_summary_table

__all__ = [
    'render_sidebar',
    'render_filters',
    'render_kpi_cards',
    'render_metric_card',
    'render_styled_table',
    'render_summary_table'
]

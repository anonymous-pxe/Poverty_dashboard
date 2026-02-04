"""
Pages module for the Poverty Dashboard.
Contains all page views for the application.
"""

from .dashboard import render_dashboard_page
from .global_trends import render_global_trends_page
from .rural_vs_urban import render_rural_vs_urban_page
from .analysis import render_analysis_page
from .visualization import render_visualization_page
from .reports import render_reports_page
from .learn_more import render_learn_more_page

__all__ = [
    'render_dashboard_page',
    'render_global_trends_page',
    'render_rural_vs_urban_page',
    'render_analysis_page',
    'render_visualization_page',
    'render_reports_page',
    'render_learn_more_page'
]

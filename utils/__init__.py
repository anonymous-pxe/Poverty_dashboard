"""
Utility module for the Poverty Dashboard.
Provides visualization, statistics, ML, and PDF generation utilities.
"""

from .visualization import (
    create_line_chart,
    create_bar_chart,
    create_box_plot,
    create_pie_chart,
    create_choropleth_map,
    create_scatter_plot,
    create_heatmap
)
from .stats import (
    calculate_summary_statistics,
    calculate_correlation,
    perform_regression,
    perform_hypothesis_test
)
from .ml import (
    train_prediction_model,
    make_predictions,
    evaluate_model,
    feature_importance
)
from .pdf_generator import generate_pdf_report

__all__ = [
    'create_line_chart',
    'create_bar_chart',
    'create_box_plot',
    'create_pie_chart',
    'create_choropleth_map',
    'create_scatter_plot',
    'create_heatmap',
    'calculate_summary_statistics',
    'calculate_correlation',
    'perform_regression',
    'perform_hypothesis_test',
    'train_prediction_model',
    'make_predictions',
    'evaluate_model',
    'feature_importance',
    'generate_pdf_report'
]

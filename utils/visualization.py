"""
Visualization utilities for creating charts and maps.
Uses Plotly for interactive visualizations.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Optional, List
import config


def create_line_chart(df: pd.DataFrame,
                     x_col: str,
                     y_col: str,
                     color_col: Optional[str] = None,
                     title: str = "Line Chart",
                     x_label: Optional[str] = None,
                     y_label: Optional[str] = None) -> go.Figure:
    """
    Create an interactive line chart.
    
    Args:
        df: DataFrame with data
        x_col: Column for x-axis
        y_col: Column for y-axis
        color_col: Optional column for color grouping
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
    
    Returns:
        plotly.graph_objects.Figure
    """
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        labels={x_col: x_label or x_col, y_col: y_label or y_col},
        height=config.CHART_HEIGHT
    )
    
    fig.update_layout(
        hovermode='x unified',
        showlegend=True,
        template='plotly_white'
    )
    
    return fig


def create_bar_chart(df: pd.DataFrame,
                    x_col: str,
                    y_col: str,
                    color_col: Optional[str] = None,
                    title: str = "Bar Chart",
                    orientation: str = 'v',
                    barmode: str = 'group') -> go.Figure:
    """
    Create an interactive bar chart.
    
    Args:
        df: DataFrame with data
        x_col: Column for x-axis
        y_col: Column for y-axis
        color_col: Optional column for color grouping
        title: Chart title
        orientation: 'v' for vertical, 'h' for horizontal
        barmode: 'group', 'stack', or 'overlay'
    
    Returns:
        plotly.graph_objects.Figure
    """
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        orientation=orientation,
        barmode=barmode,
        height=config.CHART_HEIGHT
    )
    
    fig.update_layout(
        showlegend=True,
        template='plotly_white'
    )
    
    return fig


def create_box_plot(df: pd.DataFrame,
                   x_col: Optional[str],
                   y_col: str,
                   color_col: Optional[str] = None,
                   title: str = "Box Plot") -> go.Figure:
    """
    Create a box plot for distribution analysis.
    
    Args:
        df: DataFrame with data
        x_col: Column for x-axis (categories)
        y_col: Column for y-axis (values)
        color_col: Optional column for color grouping
        title: Chart title
    
    Returns:
        plotly.graph_objects.Figure
    """
    fig = px.box(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        height=config.CHART_HEIGHT
    )
    
    fig.update_layout(
        template='plotly_white'
    )
    
    return fig


def create_pie_chart(df: pd.DataFrame,
                    names_col: str,
                    values_col: str,
                    title: str = "Pie Chart") -> go.Figure:
    """
    Create a pie chart.
    
    Args:
        df: DataFrame with data
        names_col: Column for slice names
        values_col: Column for slice values
        title: Chart title
    
    Returns:
        plotly.graph_objects.Figure
    """
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title,
        height=config.CHART_HEIGHT
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig


def create_choropleth_map(df: pd.DataFrame,
                         location_col: str,
                         value_col: str,
                         title: str = "Choropleth Map",
                         locationmode: str = 'country names',
                         color_scale: str = 'Reds') -> go.Figure:
    """
    Create a choropleth map.
    
    Args:
        df: DataFrame with data
        location_col: Column with location names
        value_col: Column with values to visualize
        title: Map title
        locationmode: 'country names' or 'USA-states' or 'geojson-id'
        color_scale: Color scale name
    
    Returns:
        plotly.graph_objects.Figure
    """
    fig = px.choropleth(
        df,
        locations=location_col,
        locationmode=locationmode,
        color=value_col,
        title=title,
        color_continuous_scale=color_scale,
        height=config.MAP_HEIGHT
    )
    
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        )
    )
    
    return fig


def create_scatter_plot(df: pd.DataFrame,
                       x_col: str,
                       y_col: str,
                       color_col: Optional[str] = None,
                       size_col: Optional[str] = None,
                       title: str = "Scatter Plot",
                       trendline: Optional[str] = None) -> go.Figure:
    """
    Create a scatter plot.
    
    Args:
        df: DataFrame with data
        x_col: Column for x-axis
        y_col: Column for y-axis
        color_col: Optional column for color
        size_col: Optional column for bubble size
        title: Chart title
        trendline: 'ols' for linear regression line
    
    Returns:
        plotly.graph_objects.Figure
    """
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        size=size_col,
        title=title,
        trendline=trendline,
        height=config.CHART_HEIGHT
    )
    
    fig.update_layout(
        template='plotly_white'
    )
    
    return fig


def create_heatmap(df: pd.DataFrame,
                  title: str = "Correlation Heatmap",
                  color_scale: str = 'RdBu_r') -> go.Figure:
    """
    Create a correlation heatmap.
    
    Args:
        df: DataFrame or correlation matrix
        title: Chart title
        color_scale: Color scale name
    
    Returns:
        plotly.graph_objects.Figure
    """
    # If df is not a correlation matrix, compute it
    if not all(df.columns == df.index):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr()
    else:
        corr_matrix = df
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale=color_scale,
        zmid=0,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title=title,
        height=config.CHART_HEIGHT,
        template='plotly_white'
    )
    
    return fig


def create_area_chart(df: pd.DataFrame,
                     x_col: str,
                     y_col: str,
                     color_col: Optional[str] = None,
                     title: str = "Area Chart") -> go.Figure:
    """
    Create an area chart.
    
    Args:
        df: DataFrame with data
        x_col: Column for x-axis
        y_col: Column for y-axis
        color_col: Optional column for color grouping
        title: Chart title
    
    Returns:
        plotly.graph_objects.Figure
    """
    fig = px.area(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        height=config.CHART_HEIGHT
    )
    
    fig.update_layout(
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig


def create_histogram(df: pd.DataFrame,
                    x_col: str,
                    color_col: Optional[str] = None,
                    title: str = "Histogram",
                    nbins: int = 30) -> go.Figure:
    """
    Create a histogram.
    
    Args:
        df: DataFrame with data
        x_col: Column for values
        color_col: Optional column for color grouping
        title: Chart title
        nbins: Number of bins
    
    Returns:
        plotly.graph_objects.Figure
    """
    fig = px.histogram(
        df,
        x=x_col,
        color=color_col,
        title=title,
        nbins=nbins,
        height=config.CHART_HEIGHT
    )
    
    fig.update_layout(
        bargap=0.1,
        template='plotly_white'
    )
    
    return fig


def create_treemap(df: pd.DataFrame,
                  path_cols: List[str],
                  values_col: str,
                  title: str = "Treemap") -> go.Figure:
    """
    Create a treemap visualization.
    
    Args:
        df: DataFrame with data
        path_cols: List of columns defining the hierarchy
        values_col: Column with values
        title: Chart title
    
    Returns:
        plotly.graph_objects.Figure
    """
    fig = px.treemap(
        df,
        path=path_cols,
        values=values_col,
        title=title,
        height=config.CHART_HEIGHT
    )
    
    return fig

"""
Data preprocessing and transformation utilities.
Handles data cleaning, filtering, and aggregation.
"""

import pandas as pd
import numpy as np
from typing import List, Optional


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess raw data.
    
    Args:
        df: Raw DataFrame
    
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    df_clean = df.copy()
    
    # Remove duplicates
    df_clean = df_clean.drop_duplicates()
    
    # Handle missing values
    # For numeric columns, fill with interpolation or mean
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df_clean[col].isnull().any():
            # Try interpolation first
            df_clean[col] = df_clean[col].interpolate(method='linear', limit_direction='both')
            # If still null, fill with mean
            df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
    
    # For categorical columns, fill with mode or 'Unknown'
    categorical_cols = df_clean.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df_clean[col].isnull().any():
            mode_val = df_clean[col].mode()
            if len(mode_val) > 0:
                df_clean[col] = df_clean[col].fillna(mode_val[0])
            else:
                df_clean[col] = df_clean[col].fillna('Unknown')
    
    # Remove outliers using IQR method for numeric columns
    for col in numeric_cols:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 3 * IQR  # Using 3*IQR for less aggressive outlier removal
        upper_bound = Q3 + 3 * IQR
        df_clean[col] = df_clean[col].clip(lower=lower_bound, upper=upper_bound)
    
    return df_clean


def filter_data(df: pd.DataFrame,
                years: Optional[List[int]] = None,
                states: Optional[List[str]] = None,
                countries: Optional[List[str]] = None,
                area_type: Optional[str] = None) -> pd.DataFrame:
    """
    Filter data based on various criteria.
    
    Args:
        df: DataFrame to filter
        years: List of years to include
        states: List of states to include
        countries: List of countries to include
        area_type: Area type to filter (Rural/Urban/Total)
    
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    df_filtered = df.copy()
    
    # Filter by years
    if years is not None and 'year' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['year'].isin(years)]
    
    # Filter by states
    if states is not None and 'state' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['state'].isin(states)]
    
    # Filter by countries
    if countries is not None:
        if 'country' in df_filtered.columns:
            df_filtered = df_filtered[df_filtered['country'].isin(countries)]
        elif 'country_code' in df_filtered.columns:
            df_filtered = df_filtered[df_filtered['country_code'].isin(countries)]
    
    # Filter by area type
    if area_type is not None and 'area_type' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['area_type'] == area_type]
    
    return df_filtered


def aggregate_data(df: pd.DataFrame,
                  group_by: List[str],
                  agg_cols: dict) -> pd.DataFrame:
    """
    Aggregate data by specified columns.
    
    Args:
        df: DataFrame to aggregate
        group_by: List of columns to group by
        agg_cols: Dictionary of {column: aggregation_function}
                 e.g., {'poverty_rate': 'mean', 'population': 'sum'}
    
    Returns:
        pd.DataFrame: Aggregated DataFrame
    """
    df_agg = df.groupby(group_by).agg(agg_cols).reset_index()
    
    # Flatten column names if multi-level
    if isinstance(df_agg.columns, pd.MultiIndex):
        df_agg.columns = ['_'.join(col).strip('_') for col in df_agg.columns.values]
    
    return df_agg


def calculate_growth_rate(df: pd.DataFrame,
                         value_col: str,
                         group_col: Optional[str] = None) -> pd.DataFrame:
    """
    Calculate year-over-year growth rate.
    
    Args:
        df: DataFrame with year and value columns
        value_col: Column name for values
        group_col: Optional column to group by (e.g., 'state', 'country')
    
    Returns:
        pd.DataFrame: DataFrame with growth_rate column added
    """
    df_sorted = df.sort_values('year').copy()
    
    if group_col:
        df_sorted['growth_rate'] = df_sorted.groupby(group_col)[value_col].pct_change() * 100
    else:
        df_sorted['growth_rate'] = df_sorted[value_col].pct_change() * 100
    
    return df_sorted


def pivot_data(df: pd.DataFrame,
              index: str,
              columns: str,
              values: str,
              aggfunc: str = 'mean') -> pd.DataFrame:
    """
    Pivot data for easier visualization.
    
    Args:
        df: DataFrame to pivot
        index: Column to use as index
        columns: Column to use as columns
        values: Column to aggregate
        aggfunc: Aggregation function
    
    Returns:
        pd.DataFrame: Pivoted DataFrame
    """
    return df.pivot_table(
        index=index,
        columns=columns,
        values=values,
        aggfunc=aggfunc
    ).reset_index()


def normalize_data(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Normalize specified columns to 0-1 range.
    
    Args:
        df: DataFrame to normalize
        columns: List of columns to normalize
    
    Returns:
        pd.DataFrame: DataFrame with normalized columns
    """
    df_norm = df.copy()
    
    for col in columns:
        if col in df_norm.columns:
            min_val = df_norm[col].min()
            max_val = df_norm[col].max()
            if max_val > min_val:
                df_norm[f'{col}_normalized'] = (df_norm[col] - min_val) / (max_val - min_val)
            else:
                df_norm[f'{col}_normalized'] = 0
    
    return df_norm


def add_moving_average(df: pd.DataFrame,
                      value_col: str,
                      window: int = 3,
                      group_col: Optional[str] = None) -> pd.DataFrame:
    """
    Add moving average column to DataFrame.
    
    Args:
        df: DataFrame with time series data
        value_col: Column to calculate moving average for
        window: Window size for moving average
        group_col: Optional column to group by
    
    Returns:
        pd.DataFrame: DataFrame with moving average column
    """
    df_sorted = df.sort_values('year').copy()
    
    if group_col:
        df_sorted[f'{value_col}_ma{window}'] = (
            df_sorted.groupby(group_col)[value_col]
            .transform(lambda x: x.rolling(window=window, min_periods=1).mean())
        )
    else:
        df_sorted[f'{value_col}_ma{window}'] = (
            df_sorted[value_col].rolling(window=window, min_periods=1).mean()
        )
    
    return df_sorted


def calculate_percentiles(df: pd.DataFrame,
                         value_col: str,
                         percentiles: List[float] = [25, 50, 75]) -> dict:
    """
    Calculate percentiles for a column.
    
    Args:
        df: DataFrame
        value_col: Column to calculate percentiles for
        percentiles: List of percentiles to calculate (0-100)
    
    Returns:
        dict: Dictionary with percentile values
    """
    result = {}
    for p in percentiles:
        result[f'p{p}'] = df[value_col].quantile(p / 100)
    return result


def create_summary_stats(df: pd.DataFrame, numeric_cols: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Create summary statistics for numeric columns.
    
    Args:
        df: DataFrame
        numeric_cols: Optional list of columns to summarize
    
    Returns:
        pd.DataFrame: Summary statistics
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    summary = df[numeric_cols].describe().T
    summary['median'] = df[numeric_cols].median()
    summary['skewness'] = df[numeric_cols].skew()
    summary['kurtosis'] = df[numeric_cols].kurtosis()
    
    return summary

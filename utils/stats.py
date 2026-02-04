"""
Statistical analysis utilities.
Provides functions for summary statistics, correlation, and regression analysis.
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from typing import Dict, List, Optional, Tuple


def calculate_summary_statistics(df: pd.DataFrame, 
                                 columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Calculate comprehensive summary statistics for numeric columns.
    
    Args:
        df: DataFrame to analyze
        columns: Optional list of columns to analyze
    
    Returns:
        pd.DataFrame: Summary statistics
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    summary_data = []
    
    for col in columns:
        data = df[col].dropna()
        
        summary_data.append({
            'Variable': col,
            'Count': len(data),
            'Mean': data.mean(),
            'Median': data.median(),
            'Std Dev': data.std(),
            'Min': data.min(),
            'Max': data.max(),
            'Q1': data.quantile(0.25),
            'Q3': data.quantile(0.75),
            'IQR': data.quantile(0.75) - data.quantile(0.25),
            'Skewness': data.skew(),
            'Kurtosis': data.kurtosis(),
            'CV (%)': (data.std() / data.mean() * 100) if data.mean() != 0 else 0
        })
    
    return pd.DataFrame(summary_data)


def calculate_correlation(df: pd.DataFrame,
                         columns: Optional[List[str]] = None,
                         method: str = 'pearson') -> pd.DataFrame:
    """
    Calculate correlation matrix.
    
    Args:
        df: DataFrame to analyze
        columns: Optional list of columns
        method: 'pearson', 'spearman', or 'kendall'
    
    Returns:
        pd.DataFrame: Correlation matrix
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    return df[columns].corr(method=method)


def perform_regression(df: pd.DataFrame,
                      x_cols: List[str],
                      y_col: str) -> Dict:
    """
    Perform linear regression analysis.
    
    Args:
        df: DataFrame with data
        x_cols: List of independent variable columns
        y_col: Dependent variable column
    
    Returns:
        dict: Regression results including coefficients, R², and predictions
    """
    # Prepare data
    X = df[x_cols].dropna()
    y = df.loc[X.index, y_col]
    
    # Fit model
    model = LinearRegression()
    model.fit(X, y)
    
    # Calculate predictions
    y_pred = model.predict(X)
    
    # Calculate metrics
    r_squared = model.score(X, y)
    mse = np.mean((y - y_pred) ** 2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(y - y_pred))
    
    # Create coefficient DataFrame
    coefficients = pd.DataFrame({
        'Variable': x_cols,
        'Coefficient': model.coef_,
        'Abs_Coefficient': np.abs(model.coef_)
    }).sort_values('Abs_Coefficient', ascending=False)
    
    return {
        'model': model,
        'coefficients': coefficients,
        'intercept': model.intercept_,
        'r_squared': r_squared,
        'mse': mse,
        'rmse': rmse,
        'mae': mae,
        'predictions': y_pred,
        'residuals': y - y_pred
    }


def perform_hypothesis_test(group1: pd.Series,
                           group2: pd.Series,
                           test_type: str = 't-test') -> Dict:
    """
    Perform hypothesis testing between two groups.
    
    Args:
        group1: First group data
        group2: Second group data
        test_type: 't-test', 'mann-whitney', or 'ks-test'
    
    Returns:
        dict: Test results with statistic and p-value
    """
    # Remove NaN values
    g1 = group1.dropna()
    g2 = group2.dropna()
    
    if test_type == 't-test':
        statistic, p_value = stats.ttest_ind(g1, g2)
        test_name = "Independent T-Test"
    elif test_type == 'mann-whitney':
        statistic, p_value = stats.mannwhitneyu(g1, g2)
        test_name = "Mann-Whitney U Test"
    elif test_type == 'ks-test':
        statistic, p_value = stats.ks_2samp(g1, g2)
        test_name = "Kolmogorov-Smirnov Test"
    else:
        raise ValueError(f"Unknown test type: {test_type}")
    
    # Determine significance
    significance = "Significant" if p_value < 0.05 else "Not Significant"
    
    return {
        'test_name': test_name,
        'statistic': statistic,
        'p_value': p_value,
        'significance': significance,
        'alpha': 0.05,
        'group1_mean': g1.mean(),
        'group2_mean': g2.mean(),
        'group1_std': g1.std(),
        'group2_std': g2.std(),
        'group1_n': len(g1),
        'group2_n': len(g2)
    }


def calculate_trend(df: pd.DataFrame,
                   time_col: str,
                   value_col: str) -> Dict:
    """
    Calculate trend using linear regression on time series.
    
    Args:
        df: DataFrame with time series data
        time_col: Column with time values (will be converted to numeric)
        value_col: Column with values
    
    Returns:
        dict: Trend analysis results
    """
    # Prepare data
    df_clean = df[[time_col, value_col]].dropna()
    
    # Convert time to numeric if needed
    if df_clean[time_col].dtype == 'object':
        x = pd.to_numeric(df_clean[time_col], errors='coerce')
    else:
        x = df_clean[time_col].values
    
    y = df_clean[value_col].values
    
    # Remove any NaN from conversion
    mask = ~(np.isnan(x) | np.isnan(y))
    x = x[mask].reshape(-1, 1)
    y = y[mask]
    
    # Fit linear model
    model = LinearRegression()
    model.fit(x, y)
    
    # Calculate trend
    slope = model.coef_[0]
    intercept = model.intercept_
    r_squared = model.score(x, y)
    
    # Determine trend direction
    if slope > 0:
        direction = "Increasing"
    elif slope < 0:
        direction = "Decreasing"
    else:
        direction = "Flat"
    
    # Calculate percentage change
    start_value = y[0]
    end_value = y[-1]
    pct_change = ((end_value - start_value) / start_value * 100) if start_value != 0 else 0
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'direction': direction,
        'start_value': start_value,
        'end_value': end_value,
        'absolute_change': end_value - start_value,
        'percent_change': pct_change
    }


def calculate_distribution_stats(series: pd.Series) -> Dict:
    """
    Calculate distribution statistics for a series.
    
    Args:
        series: Pandas Series
    
    Returns:
        dict: Distribution statistics
    """
    data = series.dropna()
    
    return {
        'mean': data.mean(),
        'median': data.median(),
        'mode': data.mode()[0] if len(data.mode()) > 0 else None,
        'std': data.std(),
        'variance': data.var(),
        'skewness': data.skew(),
        'kurtosis': data.kurtosis(),
        'min': data.min(),
        'max': data.max(),
        'range': data.max() - data.min(),
        'q1': data.quantile(0.25),
        'q2': data.quantile(0.50),
        'q3': data.quantile(0.75),
        'iqr': data.quantile(0.75) - data.quantile(0.25),
        'cv': (data.std() / data.mean() * 100) if data.mean() != 0 else 0
    }


def detect_outliers(series: pd.Series, method: str = 'iqr') -> Tuple[pd.Series, pd.Series]:
    """
    Detect outliers in a series.
    
    Args:
        series: Pandas Series
        method: 'iqr' or 'zscore'
    
    Returns:
        tuple: (outliers_boolean_mask, outlier_values)
    """
    data = series.dropna()
    
    if method == 'iqr':
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers_mask = (data < lower_bound) | (data > upper_bound)
    
    elif method == 'zscore':
        z_scores = np.abs(stats.zscore(data))
        outliers_mask = z_scores > 3
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    outlier_values = data[outliers_mask]
    
    return outliers_mask, outlier_values


def calculate_growth_metrics(df: pd.DataFrame,
                            time_col: str,
                            value_col: str,
                            group_col: Optional[str] = None) -> pd.DataFrame:
    """
    Calculate various growth metrics.
    
    Args:
        df: DataFrame with time series data
        time_col: Column with time values
        value_col: Column with values
        group_col: Optional grouping column
    
    Returns:
        pd.DataFrame: Growth metrics
    """
    df_sorted = df.sort_values(time_col).copy()
    
    if group_col:
        # Calculate for each group
        df_sorted['yoy_change'] = df_sorted.groupby(group_col)[value_col].diff()
        df_sorted['yoy_pct_change'] = df_sorted.groupby(group_col)[value_col].pct_change() * 100
        df_sorted['cumulative_change'] = df_sorted.groupby(group_col)[value_col].transform(
            lambda x: x - x.iloc[0]
        )
    else:
        # Calculate for entire dataset
        df_sorted['yoy_change'] = df_sorted[value_col].diff()
        df_sorted['yoy_pct_change'] = df_sorted[value_col].pct_change() * 100
        df_sorted['cumulative_change'] = df_sorted[value_col] - df_sorted[value_col].iloc[0]
    
    return df_sorted

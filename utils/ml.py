"""
Machine Learning utilities for poverty prediction and forecasting.
Uses scikit-learn for model training and evaluation.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Optional, Tuple
import config


def train_prediction_model(df: pd.DataFrame,
                          feature_cols: List[str],
                          target_col: str,
                          model_type: str = 'linear',
                          test_size: float = None,
                          random_state: int = None) -> Dict:
    """
    Train a prediction model.
    
    Args:
        df: DataFrame with features and target
        feature_cols: List of feature column names
        target_col: Target column name
        model_type: 'linear', 'ridge', 'lasso', 'random_forest', or 'gradient_boosting'
        test_size: Fraction of data for testing
        random_state: Random state for reproducibility
    
    Returns:
        dict: Model, predictions, and evaluation metrics
    """
    if test_size is None:
        test_size = config.TEST_SIZE
    if random_state is None:
        random_state = config.RANDOM_STATE
    
    # Prepare data
    X = df[feature_cols].dropna()
    y = df.loc[X.index, target_col]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Select model
    if model_type == 'linear':
        model = LinearRegression()
    elif model_type == 'ridge':
        model = Ridge(alpha=1.0, random_state=random_state)
    elif model_type == 'lasso':
        model = Lasso(alpha=1.0, random_state=random_state)
    elif model_type == 'random_forest':
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=random_state,
            n_jobs=-1
        )
    elif model_type == 'gradient_boosting':
        model = GradientBoostingRegressor(
            n_estimators=100,
            random_state=random_state
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Train model
    model.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)
    
    # Evaluate model
    train_metrics = _calculate_metrics(y_train, y_train_pred)
    test_metrics = _calculate_metrics(y_test, y_test_pred)
    
    # Cross-validation
    cv_scores = cross_val_score(
        model, X_train_scaled, y_train,
        cv=config.CV_FOLDS,
        scoring='r2'
    )
    
    return {
        'model': model,
        'scaler': scaler,
        'feature_cols': feature_cols,
        'target_col': target_col,
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'y_train_pred': y_train_pred,
        'y_test_pred': y_test_pred,
        'train_metrics': train_metrics,
        'test_metrics': test_metrics,
        'cv_scores': cv_scores,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }


def make_predictions(model: object,
                    scaler: object,
                    X_new: pd.DataFrame) -> np.ndarray:
    """
    Make predictions on new data.
    
    Args:
        model: Trained model
        scaler: Fitted scaler
        X_new: New data for prediction
    
    Returns:
        np.ndarray: Predictions
    """
    X_scaled = scaler.transform(X_new)
    return model.predict(X_scaled)


def evaluate_model(y_true: pd.Series, y_pred: np.ndarray) -> Dict:
    """
    Evaluate model performance.
    
    Args:
        y_true: True values
        y_pred: Predicted values
    
    Returns:
        dict: Evaluation metrics
    """
    return _calculate_metrics(y_true, y_pred)


def _calculate_metrics(y_true, y_pred) -> Dict:
    """Helper function to calculate evaluation metrics."""
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    # Calculate MAPE (Mean Absolute Percentage Error)
    # Avoid division by zero
    mask = y_true != 0
    mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100 if mask.any() else 0
    
    return {
        'mse': mse,
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'mape': mape
    }


def feature_importance(model: object,
                      feature_names: List[str]) -> pd.DataFrame:
    """
    Extract feature importance from trained model.
    
    Args:
        model: Trained model
        feature_names: List of feature names
    
    Returns:
        pd.DataFrame: Feature importance rankings
    """
    # Get feature importance based on model type
    if hasattr(model, 'feature_importances_'):
        # Tree-based models
        importances = model.feature_importances_
    elif hasattr(model, 'coef_'):
        # Linear models
        importances = np.abs(model.coef_)
    else:
        raise ValueError("Model does not support feature importance extraction")
    
    # Create DataFrame
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    # Add relative importance
    importance_df['Relative_Importance'] = (
        importance_df['Importance'] / importance_df['Importance'].sum() * 100
    )
    
    return importance_df


def forecast_time_series(df: pd.DataFrame,
                        time_col: str,
                        value_col: str,
                        periods: int = 5) -> pd.DataFrame:
    """
    Simple time series forecasting using linear regression.
    
    Args:
        df: DataFrame with time series data
        time_col: Column with time values
        value_col: Column with values to forecast
        periods: Number of periods to forecast
    
    Returns:
        pd.DataFrame: Historical data with forecasts
    """
    # Prepare data
    df_clean = df[[time_col, value_col]].dropna().copy()
    df_clean = df_clean.sort_values(time_col)
    
    # Convert time to numeric
    if df_clean[time_col].dtype == 'object':
        time_numeric = pd.to_numeric(df_clean[time_col], errors='coerce')
    else:
        time_numeric = df_clean[time_col].values
    
    X = time_numeric.values.reshape(-1, 1)
    y = df_clean[value_col].values
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Make predictions for historical data
    y_pred = model.predict(X)
    
    # Forecast future periods
    last_time = time_numeric.max()
    future_times = np.array([last_time + i for i in range(1, periods + 1)]).reshape(-1, 1)
    future_preds = model.predict(future_times)
    
    # Create results DataFrame
    historical_df = df_clean.copy()
    historical_df['prediction'] = y_pred
    historical_df['type'] = 'historical'
    
    # Create forecast DataFrame
    forecast_df = pd.DataFrame({
        time_col: future_times.flatten(),
        value_col: future_preds,
        'prediction': future_preds,
        'type': 'forecast'
    })
    
    # Combine
    result_df = pd.concat([historical_df, forecast_df], ignore_index=True)
    
    return result_df


def compare_models(df: pd.DataFrame,
                  feature_cols: List[str],
                  target_col: str,
                  model_types: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Compare multiple model types.
    
    Args:
        df: DataFrame with features and target
        feature_cols: List of feature column names
        target_col: Target column name
        model_types: List of model types to compare
    
    Returns:
        pd.DataFrame: Comparison of model performances
    """
    if model_types is None:
        model_types = ['linear', 'ridge', 'lasso', 'random_forest', 'gradient_boosting']
    
    results = []
    
    for model_type in model_types:
        try:
            result = train_prediction_model(
                df=df,
                feature_cols=feature_cols,
                target_col=target_col,
                model_type=model_type
            )
            
            results.append({
                'Model': model_type.replace('_', ' ').title(),
                'Train R²': result['train_metrics']['r2'],
                'Test R²': result['test_metrics']['r2'],
                'Train RMSE': result['train_metrics']['rmse'],
                'Test RMSE': result['test_metrics']['rmse'],
                'Train MAE': result['train_metrics']['mae'],
                'Test MAE': result['test_metrics']['mae'],
                'CV Mean R²': result['cv_mean'],
                'CV Std R²': result['cv_std']
            })
        except Exception as e:
            print(f"Error training {model_type}: {str(e)}")
            continue
    
    comparison_df = pd.DataFrame(results)
    return comparison_df.sort_values('Test R²', ascending=False)

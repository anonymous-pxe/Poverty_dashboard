"""
India Poverty API module for state-wise poverty data.
Placeholder functions for fetching India-specific poverty data.
Replace with actual API calls when ready.
"""

import pandas as pd
import numpy as np
import config


def fetch_india_poverty_data(states=None, area_type='Total', start_year=None, end_year=None):
    """
    Fetch India state-wise poverty data.
    
    PLACEHOLDER: Replace this with actual API calls to your India poverty data source.
    Could be NITI Aayog, Ministry of Statistics, or custom API.
    
    Args:
        states (list): List of state names (e.g., ['Maharashtra', 'Kerala'])
        area_type (str): 'Rural', 'Urban', or 'Total'
        start_year (int): Starting year for data
        end_year (int): Ending year for data
    
    Returns:
        pd.DataFrame: DataFrame with columns [state, year, area_type, poverty_rate, 
                      below_poverty_line, literacy_rate, unemployment_rate, 
                      per_capita_income, mpi]
    """
    # TODO: Replace with actual API call
    # Example: f"{config.INDIA_POVERTY_API_URL}/states?area={area_type}&year={start_year}:{end_year}"
    
    if states is None:
        states = config.INDIAN_STATES
    
    if start_year is None:
        start_year = 2010
    if end_year is None:
        end_year = 2023
    
    # Generate placeholder data
    data = []
    np.random.seed(42)
    
    # Base poverty rates for different states (simulated)
    base_poverty = {
        "Kerala": 7, "Goa": 9, "Himachal Pradesh": 10, "Punjab": 11,
        "Haryana": 12, "Tamil Nadu": 13, "Maharashtra": 16, "Gujarat": 17,
        "Karnataka": 18, "Andhra Pradesh": 19, "Telangana": 18, 
        "Rajasthan": 25, "West Bengal": 22, "Madhya Pradesh": 32,
        "Uttar Pradesh": 30, "Bihar": 35, "Jharkhand": 38, "Odisha": 33,
        "Chhattisgarh": 34, "Assam": 32
    }
    
    for state in states:
        base_rate = base_poverty.get(state, np.random.uniform(15, 30))
        
        # Adjust for area type
        if area_type == 'Rural':
            base_rate *= 1.3
        elif area_type == 'Urban':
            base_rate *= 0.7
        
        for year in range(start_year, end_year + 1):
            # Simulate declining poverty over time
            trend = -0.8 * ((year - start_year) / (end_year - start_year))
            noise = np.random.normal(0, 1.5)
            poverty_rate = max(1.0, base_rate + trend + noise)
            
            # Generate correlated indicators
            literacy_rate = min(99, 70 + (100 - poverty_rate) * 0.3 + np.random.normal(0, 3))
            unemployment_rate = max(1, poverty_rate * 0.2 + np.random.normal(0, 1))
            per_capita_income = 50000 + (100 - poverty_rate) * 2000 + np.random.normal(0, 5000)
            mpi = poverty_rate / 100 * 0.5 + np.random.uniform(-0.05, 0.05)
            
            # Population estimate (in millions)
            population = np.random.uniform(5, 200)
            below_poverty_line = (poverty_rate / 100) * population
            
            data.append({
                'state': state,
                'year': year,
                'area_type': area_type,
                'poverty_rate': round(poverty_rate, 2),
                'below_poverty_line': round(below_poverty_line, 2),
                'literacy_rate': round(literacy_rate, 2),
                'unemployment_rate': round(unemployment_rate, 2),
                'per_capita_income': round(per_capita_income, 2),
                'mpi': round(mpi, 3)
            })
    
    df = pd.DataFrame(data)
    return df


def get_india_states():
    """
    Get list of Indian states with metadata.
    
    PLACEHOLDER: Replace with actual API call.
    
    Returns:
        pd.DataFrame: DataFrame with state information
    """
    # TODO: Replace with actual API call
    
    states_data = []
    for state in config.INDIAN_STATES:
        states_data.append({
            'state': state,
            'region': _get_region(state),
            'capital': _get_capital(state)
        })
    
    return pd.DataFrame(states_data)


def _get_region(state):
    """Helper function to get region for a state."""
    regions = {
        'North': ['Punjab', 'Haryana', 'Himachal Pradesh', 'Uttarakhand', 'Uttar Pradesh'],
        'South': ['Karnataka', 'Kerala', 'Tamil Nadu', 'Andhra Pradesh', 'Telangana'],
        'East': ['West Bengal', 'Odisha', 'Bihar', 'Jharkhand'],
        'West': ['Gujarat', 'Maharashtra', 'Rajasthan', 'Goa'],
        'Northeast': ['Assam', 'Arunachal Pradesh', 'Nagaland', 'Manipur', 'Mizoram', 
                     'Tripura', 'Meghalaya', 'Sikkim'],
        'Central': ['Madhya Pradesh', 'Chhattisgarh']
    }
    
    for region, states in regions.items():
        if state in states:
            return region
    return 'Other'


def _get_capital(state):
    """Helper function to get capital for a state."""
    capitals = {
        'Andhra Pradesh': 'Amaravati',
        'Arunachal Pradesh': 'Itanagar',
        'Assam': 'Dispur',
        'Bihar': 'Patna',
        'Chhattisgarh': 'Raipur',
        'Goa': 'Panaji',
        'Gujarat': 'Gandhinagar',
        'Haryana': 'Chandigarh',
        'Himachal Pradesh': 'Shimla',
        'Jharkhand': 'Ranchi',
        'Karnataka': 'Bengaluru',
        'Kerala': 'Thiruvananthapuram',
        'Madhya Pradesh': 'Bhopal',
        'Maharashtra': 'Mumbai',
        'Manipur': 'Imphal',
        'Meghalaya': 'Shillong',
        'Mizoram': 'Aizawl',
        'Nagaland': 'Kohima',
        'Odisha': 'Bhubaneswar',
        'Punjab': 'Chandigarh',
        'Rajasthan': 'Jaipur',
        'Sikkim': 'Gangtok',
        'Tamil Nadu': 'Chennai',
        'Telangana': 'Hyderabad',
        'Tripura': 'Agartala',
        'Uttar Pradesh': 'Lucknow',
        'Uttarakhand': 'Dehradun',
        'West Bengal': 'Kolkata'
    }
    return capitals.get(state, 'Unknown')


def fetch_india_rural_urban_comparison(states=None, year=None):
    """
    Fetch rural vs urban poverty comparison for Indian states.
    
    Args:
        states (list): List of state names
        year (int): Specific year for comparison
    
    Returns:
        pd.DataFrame: DataFrame with rural and urban poverty rates
    """
    if year is None:
        year = 2023
    
    if states is None:
        states = config.INDIAN_STATES
    
    # Fetch both rural and urban data
    rural_data = fetch_india_poverty_data(states=states, area_type='Rural', 
                                          start_year=year, end_year=year)
    urban_data = fetch_india_poverty_data(states=states, area_type='Urban',
                                          start_year=year, end_year=year)
    
    # Merge the data
    comparison = pd.merge(
        rural_data[['state', 'year', 'poverty_rate']].rename(columns={'poverty_rate': 'rural_poverty'}),
        urban_data[['state', 'year', 'poverty_rate']].rename(columns={'poverty_rate': 'urban_poverty'}),
        on=['state', 'year']
    )
    
    comparison['difference'] = comparison['rural_poverty'] - comparison['urban_poverty']
    comparison['ratio'] = comparison['rural_poverty'] / comparison['urban_poverty']
    
    return comparison

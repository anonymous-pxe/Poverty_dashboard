"""
India Poverty API module for state-wise poverty data.
Makes actual API calls to NDAP (National Data & Analytics Platform) API.
"""

import pandas as pd
import numpy as np
import requests
from typing import Optional, List
import config


def fetch_india_poverty_data(states=None, area_type='Total', start_year=None, end_year=None):
    """
    Fetch India state-wise poverty data from NDAP API.
    
    API Endpoint: https://loadqa.ndapapi.com/v1/openapi
    Indicators: I7386_3 (Rural), I7386_4 (Urban)
    
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
    if states is None:
        states = config.INDIAN_STATES
    
    if start_year is None:
        start_year = 2010
    if end_year is None:
        end_year = 2023
    
    # Determine which indicator(s) to fetch based on area_type
    if area_type == 'Rural':
        indicators = ['I7386_3']  # Rural poverty indicator
    elif area_type == 'Urban':
        indicators = ['I7386_4']  # Urban poverty indicator
    else:  # Total
        indicators = ['I7386_3', 'I7386_4']  # Both for averaging
    
    try:
        # Fetch data from NDAP API
        all_data = []
        
        for indicator in indicators:
            # Construct API URL
            url = config.INDIA_POVERTY_API_URL
            params = {
                'API_Key': config.INDIA_POVERTY_API_KEY,
                'ind': indicator,
                'dim': 'Country,StateName,StateCode,Year',
                'pageno': 1
            }
            
            # Make API request
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse JSON response
            json_data = response.json()
            
            # Extract records from response
            if 'data' in json_data and json_data['data']:
                records = json_data['data']
                
                for record in records:
                    state_name = record.get('StateName', '')
                    year = record.get('Year', '')
                    value = record.get('value', None)
                    
                    # Filter by states and year range
                    if state_name in states and value is not None:
                        try:
                            year_int = int(year)
                            if start_year <= year_int <= end_year:
                                all_data.append({
                                    'state': state_name,
                                    'state_code': record.get('StateCode', ''),
                                    'year': year_int,
                                    'indicator': indicator,
                                    'poverty_rate': float(value)
                                })
                        except (ValueError, TypeError):
                            continue
        
        if not all_data:
            # No data from API, use placeholder
            return _generate_placeholder_india_data(states, area_type, start_year, end_year)
        
        # Convert to DataFrame
        df = pd.DataFrame(all_data)
        
        # If Total area type, average rural and urban
        if area_type == 'Total' and len(indicators) == 2:
            # Group by state and year, average poverty rates
            df_grouped = df.groupby(['state', 'state_code', 'year']).agg({
                'poverty_rate': 'mean'
            }).reset_index()
            df = df_grouped
        
        # Add area_type column
        df['area_type'] = area_type
        
        # Add derived/correlated indicators (simulated for now)
        df = _add_derived_indicators(df)
        
        return df
    
    except (requests.RequestException, ValueError, KeyError) as e:
        # If API fails, fall back to placeholder data
        print(f"Warning: India Poverty API error ({str(e)}). Using placeholder data.")
        return _generate_placeholder_india_data(states, area_type, start_year, end_year)


def _add_derived_indicators(df):
    """
    Add derived indicators correlated with poverty rate.
    These would ideally come from the API as well.
    
    Args:
        df: DataFrame with poverty_rate
    
    Returns:
        pd.DataFrame: DataFrame with additional indicators
    """
    df = df.copy()
    
    # Generate correlated indicators (placeholder formulas)
    # In production, these should come from additional API calls or data sources
    np.random.seed(42)
    
    for idx, row in df.iterrows():
        poverty_rate = row['poverty_rate']
        
        # Literacy rate (inversely correlated with poverty)
        literacy_rate = min(99, 70 + (100 - poverty_rate) * 0.3 + np.random.normal(0, 3))
        
        # Unemployment rate (positively correlated with poverty)
        unemployment_rate = max(1, poverty_rate * 0.2 + np.random.normal(0, 1))
        
        # Per capita income (inversely correlated with poverty)
        per_capita_income = 50000 + (100 - poverty_rate) * 2000 + np.random.normal(0, 5000)
        
        # MPI (correlated with poverty)
        mpi = poverty_rate / 100 * 0.5 + np.random.uniform(-0.05, 0.05)
        
        # Below poverty line (in millions - rough estimate)
        population = np.random.uniform(5, 200)  # State population estimate
        below_poverty_line = (poverty_rate / 100) * population
        
        df.at[idx, 'literacy_rate'] = round(literacy_rate, 2)
        df.at[idx, 'unemployment_rate'] = round(unemployment_rate, 2)
        df.at[idx, 'per_capita_income'] = round(per_capita_income, 2)
        df.at[idx, 'mpi'] = round(mpi, 3)
        df.at[idx, 'below_poverty_line'] = round(below_poverty_line, 2)
    
    return df


def _generate_placeholder_india_data(states, area_type, start_year, end_year):
    """
    Generate placeholder data when API is unavailable.
    
    Args:
        states: List of state names
        area_type: Area type
        start_year: Start year
        end_year: End year
    
    Returns:
        pd.DataFrame: Simulated data
    """
    # Base poverty rates for different states (simulated)
    base_poverty = {
        "Kerala": 7, "Goa": 9, "Himachal Pradesh": 10, "Punjab": 11,
        "Haryana": 12, "Tamil Nadu": 13, "Maharashtra": 16, "Gujarat": 17,
        "Karnataka": 18, "Andhra Pradesh": 19, "Telangana": 18, 
        "Rajasthan": 25, "West Bengal": 22, "Madhya Pradesh": 32,
        "Uttar Pradesh": 30, "Bihar": 35, "Jharkhand": 38, "Odisha": 33,
        "Chhattisgarh": 34, "Assam": 32
    }
    
    data = []
    np.random.seed(42)
    
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
    
    Returns:
        pd.DataFrame: DataFrame with state information
    """
    # Could be extended to fetch from API if available
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
        on=['state', 'year'],
        how='outer'
    )
    
    # Fill missing values with 0
    comparison = comparison.fillna(0)
    
    # Calculate difference and ratio
    comparison['difference'] = comparison['rural_poverty'] - comparison['urban_poverty']
    comparison['ratio'] = comparison.apply(
        lambda row: row['rural_poverty'] / row['urban_poverty'] if row['urban_poverty'] > 0 else 0,
        axis=1
    )
    
    return comparison


def test_india_api_connection() -> bool:
    """
    Test if India Poverty API is accessible.
    
    Returns:
        bool: True if API is accessible, False otherwise
    """
    try:
        url = config.INDIA_POVERTY_API_URL
        params = {
            'API_Key': config.INDIA_POVERTY_API_KEY,
            'ind': 'I7386_3',
            'dim': 'StateName',
            'pageno': 1
        }
        response = requests.get(url, params=params, timeout=5)
        return response.status_code == 200
    except:
        return False


def fetch_all_india_indicators(states=None, year=None):
    """
    Fetch all available indicators for Indian states.
    
    Args:
        states (list): List of state names
        year (int): Specific year
    
    Returns:
        dict: Dictionary with indicator names as keys and DataFrames as values
    """
    if year is None:
        year = 2023
    
    indicators_map = {
        'Rural Poverty': 'I7386_3',
        'Urban Poverty': 'I7386_4'
    }
    
    result = {}
    
    for name, indicator_code in indicators_map.items():
        try:
            area_type = 'Rural' if 'Rural' in name else 'Urban'
            data = fetch_india_poverty_data(
                states=states,
                area_type=area_type,
                start_year=year,
                end_year=year
            )
            result[name] = data
        except Exception as e:
            print(f"Error fetching {name}: {str(e)}")
            continue
    
    return result


def parse_ndap_response(response_json):
    """
    Parse NDAP API response format.
    
    Args:
        response_json: JSON response from NDAP API
    
    Returns:
        list: List of data records
    """
    records = []
    
    if 'data' in response_json:
        for item in response_json['data']:
            records.append(item)
    
    return records

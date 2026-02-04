"""
Configuration file for the Poverty Dashboard.
Contains constants, indicator lists, and app settings.
"""

# App Configuration
APP_TITLE = "🌍 Poverty Dashboard"
APP_ICON = "🌍"
PAGE_LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# Data Sources
WORLD_BANK_API_URL = "https://api.worldbank.org/v2"
INDIA_POVERTY_API_URL = "https://loadqa.ndapapi.com/v1/openapi"
INDIA_POVERTY_API_KEY = "gAAAAABpg20RfAwUAEq8ibudPDW7_cLCZrmUjpOVRH0W4rwwewM09vTDi1LxAXKkpRr0DaS7GES5iu9XzDOeGk-FEpMJgIL06oZ1WTR9HCrw6cmJbJvXKVKlo3VaaCkwfSaIimDLObK9RX3kl6RmWWEF88VvEpKj5ZxO-JoQzSWp2go-_rexphfoj49OMGDEVPAG25wIMFUW"

# Cache Settings
CACHE_TTL = 3600  # 1 hour in seconds

# Date Range
START_YEAR = 1990
END_YEAR = 2023

# India States
INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal"
]

# Area Types
AREA_TYPES = ["Rural", "Urban", "Total"]

# Global Poverty Indicators
GLOBAL_INDICATORS = {
    "SI.POV.DDAY": "Poverty headcount ratio at $2.15 a day (2017 PPP) (% of population)",
    "SI.POV.LMIC": "Poverty headcount ratio at $3.65 a day (2017 PPP) (% of population)",
    "SI.POV.UMIC": "Poverty headcount ratio at $6.85 a day (2017 PPP) (% of population)",
    "SI.POV.GINI": "Gini index",
    "NY.GDP.PCAP.CD": "GDP per capita (current US$)",
    "SP.POP.TOTL": "Population, total",
}

# India Poverty Indicators
INDIA_INDICATORS = [
    "Poverty Rate (%)",
    "Below Poverty Line (millions)",
    "Literacy Rate (%)",
    "Unemployment Rate (%)",
    "Per Capita Income (₹)",
    "Multidimensional Poverty Index"
]

# Color Schemes
COLOR_PALETTE = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ecc71",
    "danger": "#e74c3c",
    "warning": "#f39c12",
    "info": "#3498db",
    "rural": "#27ae60",
    "urban": "#e67e22",
}

# Chart Settings
CHART_HEIGHT = 500
MAP_HEIGHT = 600

# ML Model Settings
TEST_SIZE = 0.2
RANDOM_STATE = 42
CV_FOLDS = 5

# Export Settings
REPORTS_DIR = "reports/generated"
EXPORTS_DIR = "reports/exports"

# Page Titles
PAGE_TITLES = {
    "Dashboard": "📊 Overview Dashboard",
    "Global Trends": "🌐 Global Poverty Trends",
    "Rural vs Urban": "🏘️ Rural vs Urban Comparison",
    "Analysis": "📈 Statistical Analysis",
    "Visualization": "📉 Data Visualization",
    "Reports": "📄 Reports & Export",
    "Learn More": "📚 Learn More"
}

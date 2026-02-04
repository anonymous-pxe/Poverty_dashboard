# 🌍 Poverty Dashboard

A comprehensive data analysis and visualization platform for exploring poverty indicators across global and India-specific datasets.

## 📋 Features

- **📊 Interactive Dashboard**: Overview with key performance indicators and highlights
- **🌐 Global Trends**: Worldwide poverty indicators analysis over time
- **🏘️ Rural vs Urban Comparison**: Compare poverty rates between rural and urban areas
- **📈 Statistical Analysis**: Advanced statistical methods including correlation, regression, and trend analysis
- **📉 Custom Visualizations**: Create interactive charts with multiple chart types
- **📄 Report Generation**: Export data to CSV, Excel, and PDF formats
- **🤖 Machine Learning**: Predictive models for poverty forecasting
- **📚 Comprehensive Documentation**: Learn about methodology, data sources, and usage

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Poverty_dashboard.git
cd Poverty_dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
Poverty_dashboard/
│
├── app.py                         # Main Streamlit entry point
├── requirements.txt                # All dependencies pinned
├── config.py                       # App config, constants, indicator lists
│
├── data/
│   ├── __init__.py
│   ├── wb_api.py                   # World Bank global poverty data (placeholder API calls)
│   ├── india_poverty_api.py        # India state-wise poverty data (placeholder API calls)
│   ├── data_loader.py              # Unified data fetching & caching
│   └── preprocess.py               # Cleaning, filtering, transformations
│
├── pages/
│   ├── __init__.py
│   ├── dashboard.py                # Overview KPIs + highlights
│   ├── global_trends.py            # Global poverty trends visualization
│   ├── rural_vs_urban.py           # Rural vs Urban poverty comparison
│   ├── analysis.py                 # Statistical analysis (summary stats, correlation, regression)
│   ├── visualization.py            # Charts & maps
│   ├── reports.py                  # Downloads & PDF generation
│   └── learn_more.py               # Project info, methodology, data sources
│
├── components/
│   ├── __init__.py
│   ├── sidebar.py                  # Navigation + filters
│   ├── filters.py                  # Year, state, area, indicator filters
│   ├── metrics.py                  # KPI cards
│   └── tables.py                   # Styled data tables
│
├── utils/
│   ├── __init__.py
│   ├── visualization.py            # Line, bar, box, pie, choropleth
│   ├── stats.py                    # Summary stats, correlation, regression
│   ├── ml.py                       # ML models & predictions
│   └── pdf_generator.py            # Report → PDF export
│
├── assets/
│   ├── css/style.css               # Custom polished UI/UX
│   ├── images/                     # Images and logos
│   └── geojson/                    # Geographic data files
│
├── reports/
│   ├── generated/                  # Auto-generated PDFs
│   └── exports/                    # CSV / Excel downloads
│
└── README.md                       # This file
```

## 🎯 Usage

### Navigation

Use the sidebar to navigate between different pages:
- **Dashboard**: Get a quick overview of key metrics
- **Global Trends**: Explore worldwide poverty trends
- **Rural vs Urban**: Compare poverty across different area types
- **Analysis**: Perform statistical analysis
- **Visualization**: Create custom charts
- **Reports**: Export and download data
- **Learn More**: Read documentation

### Filters

Most pages include filters to:
- Select specific years or year ranges
- Choose states or countries
- Filter by area type (Rural/Urban/Total)
- Select specific indicators

### Exporting Data

1. Navigate to the **Reports** page
2. Select the data you want to export
3. Choose your export format (CSV, Excel, or PDF)
4. Click the download button

## 📊 Data Sources

### Global Data
- **World Bank Open Data**: Poverty indicators for 195+ countries
- **Indicators**: Poverty headcount ratios, Gini index, GDP per capita
- **Time Period**: 1990-2023

### India Data
- **NITI Aayog**: State-level poverty statistics
- **Ministry of Statistics**: Employment and economic indicators
- **Indicators**: Poverty rate, literacy rate, unemployment, per capita income, MPI
- **Coverage**: 28 states and 8 union territories

## 🔬 Analysis Capabilities

### Statistical Methods
- Descriptive statistics
- Correlation analysis (Pearson, Spearman, Kendall)
- Linear and multiple regression
- Trend analysis
- Hypothesis testing

### Machine Learning Models
- Linear Regression
- Ridge Regression
- Lasso Regression
- Random Forest
- Gradient Boosting

### Visualizations
- Line charts for trends
- Bar charts for comparisons
- Box plots for distributions
- Scatter plots for correlations
- Heatmaps for correlation matrices
- Choropleth maps for geographic data

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Statistics**: SciPy
- **Machine Learning**: Scikit-learn
- **Geographic Data**: GeoPandas
- **Reports**: ReportLab, OpenPyXL

## ⚠️ Important Notes

**Placeholder Data**: This dashboard currently uses placeholder data generated by simulation functions. For production use:

1. Replace the placeholder functions in `data/wb_api.py` with actual World Bank API calls
2. Replace the placeholder functions in `data/india_poverty_api.py` with actual India poverty data API calls
3. Update the API endpoints in `config.py`

### Integrating Real APIs

#### World Bank API
```python
# In data/wb_api.py, replace placeholder with:
import requests

def fetch_world_bank_data(indicator, country_codes, start_year, end_year):
    url = f"{config.WORLD_BANK_API_URL}/country/{';'.join(country_codes)}/indicator/{indicator}"
    params = {
        'format': 'json',
        'date': f'{start_year}:{end_year}',
        'per_page': 1000
    }
    response = requests.get(url, params=params)
    # Parse and return data
```

#### India Poverty API
```python
# In data/india_poverty_api.py, replace placeholder with actual API endpoint
import requests

def fetch_india_poverty_data(states, area_type, start_year, end_year):
    # Replace with actual India poverty data API
    url = config.INDIA_POVERTY_API_URL
    # Make API call and return data
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🙏 Acknowledgments

- World Bank for providing open data APIs
- Streamlit for the amazing framework
- All contributors and users of this dashboard

## 📚 Citation

If you use this dashboard in your research or publications, please cite:

```
Poverty Dashboard (2024). Interactive Poverty Analysis Platform.
Available at: https://github.com/yourusername/Poverty_dashboard
```

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Built with**: ❤️ and Streamlit

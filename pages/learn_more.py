"""
Learn More page - Project information, methodology, and data sources.
"""

import streamlit as st


def render_learn_more_page():
    """Render the learn more page with project information."""
    st.title("📚 Learn More")
    st.markdown("### About the Poverty Dashboard")
    
    # Overview
    st.markdown("---")
    st.header("📖 Overview")
    st.markdown("""
    The **Poverty Dashboard** is a comprehensive data analysis and visualization platform designed to provide
    insights into poverty indicators across global and India-specific datasets. This tool enables policymakers,
    researchers, and analysts to explore poverty trends, compare regional disparities, and make data-driven decisions.
    
    **Key Features:**
    - 📊 Interactive visualizations and charts
    - 🌍 Global poverty trend analysis
    - 🏘️ Rural vs Urban poverty comparison
    - 📈 Statistical analysis and correlations
    - 🤖 Machine learning predictions
    - 📄 Report generation and data export
    """)
    
    # Methodology
    st.markdown("---")
    st.header("🔬 Methodology")
    
    with st.expander("📊 Data Collection", expanded=False):
        st.markdown("""
        **Data Sources:**
        - **Global Data**: World Bank Open Data API
        - **India Data**: National statistical agencies and state-level poverty surveys
        
        **Data Collection Process:**
        1. Automated data fetching from API endpoints
        2. Data validation and quality checks
        3. Preprocessing and cleaning
        4. Regular updates to ensure currency
        
        **Data Coverage:**
        - Time Period: 1990 - 2023
        - Geographic Coverage: Global (195+ countries) and India (28 states)
        - Update Frequency: Annual
        """)
    
    with st.expander("📈 Statistical Methods", expanded=False):
        st.markdown("""
        **Analysis Techniques:**
        
        1. **Descriptive Statistics**
           - Mean, median, standard deviation
           - Percentiles and quartiles
           - Distribution analysis
        
        2. **Correlation Analysis**
           - Pearson correlation coefficient
           - Spearman rank correlation
           - Kendall tau correlation
        
        3. **Regression Analysis**
           - Linear regression
           - Multiple regression
           - Ridge and Lasso regression
        
        4. **Trend Analysis**
           - Time series decomposition
           - Linear trend fitting
           - Growth rate calculations
        
        5. **Hypothesis Testing**
           - T-tests for group comparisons
           - Mann-Whitney U test
           - Kolmogorov-Smirnov test
        """)
    
    with st.expander("🤖 Machine Learning Models", expanded=False):
        st.markdown("""
        **Predictive Models:**
        
        1. **Linear Regression**
           - Simple interpretability
           - Baseline model for comparisons
        
        2. **Ridge Regression**
           - L2 regularization
           - Handles multicollinearity
        
        3. **Lasso Regression**
           - L1 regularization
           - Feature selection capability
        
        4. **Random Forest**
           - Ensemble learning
           - Handles non-linear relationships
        
        5. **Gradient Boosting**
           - Sequential ensemble method
           - High predictive accuracy
        
        **Model Evaluation:**
        - R² Score
        - Root Mean Squared Error (RMSE)
        - Mean Absolute Error (MAE)
        - Cross-validation scores
        """)
    
    # Data Sources
    st.markdown("---")
    st.header("📊 Data Sources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌍 Global Data")
        st.markdown("""
        **World Bank Open Data**
        - Source: https://data.worldbank.org
        - API: https://datahelpdesk.worldbank.org/knowledgebase/topics/125589
        
        **Key Indicators:**
        - Poverty headcount ratio at $2.15/day
        - Poverty headcount ratio at $3.65/day
        - Poverty headcount ratio at $6.85/day
        - Gini index
        - GDP per capita
        
        **Coverage:**
        - 195+ countries and territories
        - Annual data from 1990-2023
        """)
    
    with col2:
        st.subheader("🇮🇳 India Data")
        st.markdown("""
        **National Sources**
        - NITI Aayog
        - Ministry of Statistics and Programme Implementation
        - State Government Statistical Departments
        
        **Key Indicators:**
        - State-wise poverty rates
        - Rural vs Urban poverty
        - Literacy rates
        - Unemployment rates
        - Per capita income
        - Multidimensional Poverty Index (MPI)
        
        **Coverage:**
        - 28 states and 8 union territories
        - Annual and quinquennial surveys
        """)
    
    # Technical Details
    st.markdown("---")
    st.header("⚙️ Technical Details")
    
    with st.expander("🛠️ Technology Stack", expanded=False):
        st.markdown("""
        **Frontend & Visualization:**
        - **Streamlit**: Web application framework
        - **Plotly**: Interactive visualizations
        - **Matplotlib/Seaborn**: Statistical plots
        
        **Data Processing:**
        - **Pandas**: Data manipulation and analysis
        - **NumPy**: Numerical computations
        - **SciPy**: Statistical functions
        
        **Machine Learning:**
        - **Scikit-learn**: ML models and evaluation
        - **StandardScaler**: Feature normalization
        
        **Geographic Visualization:**
        - **GeoPandas**: Geospatial data handling
        - **Plotly Choropleth**: Interactive maps
        
        **Report Generation:**
        - **ReportLab**: PDF generation
        - **OpenPyXL**: Excel export
        """)
    
    with st.expander("📁 Project Structure", expanded=False):
        st.code("""
Poverty_dashboard/
│
├── app.py                      # Main application entry point
├── config.py                   # Configuration and constants
├── requirements.txt            # Python dependencies
│
├── data/                       # Data fetching and processing
│   ├── wb_api.py              # World Bank API client
│   ├── india_poverty_api.py   # India data API client
│   ├── data_loader.py         # Data loading with caching
│   └── preprocess.py          # Data preprocessing utilities
│
├── utils/                      # Utility functions
│   ├── visualization.py       # Chart creation functions
│   ├── stats.py              # Statistical analysis
│   ├── ml.py                 # Machine learning models
│   └── pdf_generator.py      # Report generation
│
├── components/                 # Reusable UI components
│   ├── sidebar.py            # Navigation sidebar
│   ├── filters.py            # Filter components
│   ├── metrics.py            # KPI cards
│   └── tables.py             # Styled tables
│
├── pages/                      # Application pages
│   ├── dashboard.py          # Overview dashboard
│   ├── global_trends.py      # Global poverty trends
│   ├── rural_vs_urban.py     # Rural vs Urban comparison
│   ├── analysis.py           # Statistical analysis
│   ├── visualization.py      # Interactive charts
│   ├── reports.py            # Report generation
│   └── learn_more.py         # Documentation
│
├── assets/                     # Static assets
│   ├── css/style.css         # Custom styling
│   └── images/               # Images and logos
│
└── reports/                    # Generated reports
    ├── generated/            # PDF reports
    └── exports/              # CSV/Excel exports
        """, language="text")
    
    # Usage Guide
    st.markdown("---")
    st.header("📖 Usage Guide")
    
    with st.expander("🚀 Getting Started", expanded=False):
        st.markdown("""
        **Quick Start:**
        
        1. **Navigate** using the sidebar to explore different pages
        2. **Apply filters** to select specific regions, years, or indicators
        3. **View visualizations** to understand trends and patterns
        4. **Export data** for further analysis or reporting
        
        **Page Overview:**
        - **Dashboard**: Overview with key metrics and highlights
        - **Global Trends**: Worldwide poverty indicators over time
        - **Rural vs Urban**: Compare poverty rates by area type
        - **Analysis**: Statistical analysis and correlations
        - **Visualization**: Create custom charts and plots
        - **Reports**: Generate and export reports
        - **Learn More**: Project documentation (you are here)
        """)
    
    with st.expander("🔍 Tips & Best Practices", expanded=False):
        st.markdown("""
        **Data Exploration:**
        - Start with the Dashboard for a quick overview
        - Use filters to focus on specific regions or time periods
        - Compare multiple states or countries to identify patterns
        
        **Visualization:**
        - Choose appropriate chart types for your data
        - Use line charts for trends over time
        - Use bar charts for comparisons
        - Use scatter plots to explore relationships
        
        **Analysis:**
        - Check correlation before running regression
        - Validate statistical significance (p-value < 0.05)
        - Consider multiple models for prediction
        
        **Reporting:**
        - Export data in the format that best suits your needs
        - Generate PDF reports for formal presentations
        - Use CSV/Excel for further analysis in other tools
        """)
    
    # Citation
    st.markdown("---")
    st.header("📝 Citation")
    
    st.markdown("""
    If you use this dashboard or its data in your research or publications, please cite:
    
    ```
    Poverty Dashboard (2024). Interactive Poverty Analysis Platform.
    Available at: https://github.com/your-repo/poverty-dashboard
    ```
    """)
    
    # Contact & Support
    st.markdown("---")
    st.header("📧 Contact & Support")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **For Questions:**
        - Email: support@povertydashboard.org
        - GitHub Issues: Report bugs or request features
        """)
    
    with col2:
        st.markdown("""
        **Resources:**
        - Documentation: Full user guide
        - API Reference: For developers
        - Tutorials: Step-by-step guides
        """)
    
    # Disclaimer
    st.markdown("---")
    st.info("""
    **Disclaimer:** This dashboard uses placeholder data for demonstration purposes. 
    For production use, replace the placeholder API functions with actual data sources. 
    The data and analysis are provided for informational purposes only and should not be 
    used as the sole basis for policy decisions without additional validation.
    """)
    
    # Version Info
    st.markdown("---")
    st.caption("Poverty Dashboard v1.0.0 | © 2024 | Built with Streamlit")

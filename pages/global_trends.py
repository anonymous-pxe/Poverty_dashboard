"""
Global Trends page - Worldwide poverty indicators over time.
"""

import streamlit as st
from data.data_loader import load_global_data, load_countries_metadata
from components.filters import render_filters
from components.tables import render_styled_table
from utils.visualization import create_line_chart, create_choropleth_map, create_area_chart
import config


def render_global_trends_page():
    """Render the global poverty trends page."""
    st.title("🌐 Global Poverty Trends")
    st.markdown("### Worldwide poverty indicators and regional analysis")
    
    # Filters
    filters = render_filters(
        show_year=True,
        show_state=False,
        show_country=True,
        show_area=False,
        show_indicator=True
    )
    
    year_range = filters.get('year_range', (2010, 2023))
    countries = filters.get('countries', ['IND', 'CHN', 'BRA', 'ZAF'])
    indicator = filters.get('indicator', 'SI.POV.DDAY')
    
    if not countries:
        st.warning("Please select at least one country to display data.")
        return
    
    # Load data
    try:
        with st.spinner("Loading global data..."):
            global_data = load_global_data(
                indicator=indicator,
                country_codes=countries,
                start_year=year_range[0],
                end_year=year_range[1]
            )
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    if global_data.empty:
        st.warning("No data available for selected filters.")
        return
    
    # Main visualization tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Time Series", 
        "🗺️ Geographic Map", 
        "📊 Comparison", 
        "📋 Data Table"
    ])
    
    with tab1:
        st.subheader("Poverty Trends Over Time")
        
        # Line chart
        fig = create_line_chart(
            df=global_data,
            x_col='year',
            y_col='value',
            color_col='country',
            title=f'{config.GLOBAL_INDICATORS[indicator]} - Time Series',
            x_label='Year',
            y_label='Value'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Area chart for cumulative view
        st.markdown("---")
        st.subheader("Cumulative View")
        fig_area = create_area_chart(
            df=global_data,
            x_col='year',
            y_col='value',
            color_col='country',
            title='Cumulative Poverty Trends'
        )
        st.plotly_chart(fig_area, use_container_width=True)
    
    with tab2:
        st.subheader("Geographic Distribution")
        
        # Select year for map
        selected_year = st.selectbox(
            "Select Year for Map View",
            options=sorted(global_data['year'].unique(), reverse=True)
        )
        
        map_data = global_data[global_data['year'] == selected_year]
        
        # Choropleth map
        fig_map = create_choropleth_map(
            df=map_data,
            location_col='country',
            value_col='value',
            title=f'Global Poverty Distribution - {selected_year}',
            locationmode='country names',
            color_scale='Reds'
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Regional statistics
        st.markdown("---")
        st.subheader(f"Statistics for {selected_year}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Countries", len(map_data))
        with col2:
            st.metric("Average", f"{map_data['value'].mean():.2f}%")
        with col3:
            st.metric("Highest", f"{map_data['value'].max():.2f}%")
        with col4:
            st.metric("Lowest", f"{map_data['value'].min():.2f}%")
    
    with tab3:
        st.subheader("Country Comparison")
        
        # Latest year comparison
        latest_year = global_data['year'].max()
        latest_data = global_data[global_data['year'] == latest_year]
        
        from utils.visualization import create_bar_chart
        fig_bar = create_bar_chart(
            df=latest_data,
            x_col='country',
            y_col='value',
            title=f'Poverty Rates by Country ({latest_year})',
            orientation='v'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Year-over-year changes
        st.markdown("---")
        st.subheader("Year-over-Year Changes")
        
        # Data already has yoy_change and yoy_pct_change columns from load_global_data
        latest_growth = global_data[global_data['year'] == latest_year][
            ['country', 'value', 'yoy_change', 'yoy_pct_change']
        ].round(2)
        
        render_styled_table(latest_growth, title=f"Changes from Previous Year")
    
    with tab4:
        st.subheader("Complete Data Table")
        
        # Pivot table for better view
        from data.preprocess import pivot_data
        pivot = pivot_data(
            df=global_data,
            index='year',
            columns='country',
            values='value',
            aggfunc='mean'
        )
        
        render_styled_table(pivot, title="Poverty Rates by Country and Year")
        
        # Download option
        st.markdown("---")
        csv = global_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Full Data as CSV",
            data=csv,
            file_name=f"global_poverty_data_{year_range[0]}_{year_range[1]}.csv",
            mime="text/csv"
        )
    
    # Insights section
    st.markdown("---")
    st.subheader("💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Best performer
        best_country_idx = latest_data['value'].idxmin()
        best_country = latest_data.loc[best_country_idx, 'country']
        best_value = latest_data.loc[best_country_idx, 'value']
        
        st.success(f"""
        **Lowest Poverty Rate:** {best_country}  
        Rate: {best_value:.2f}%
        """)
        
        # Most improved
        if 'yoy_pct_change' in global_data.columns:
            latest_growth_complete = global_data[
                (global_data['year'] == latest_year) &
                (global_data['yoy_pct_change'].notna())
            ]
            if not latest_growth_complete.empty:
                most_improved_idx = latest_growth_complete['yoy_pct_change'].idxmin()
                most_improved = latest_growth_complete.loc[most_improved_idx, 'country']
                improvement = latest_growth_complete.loc[most_improved_idx, 'yoy_pct_change']
                
                st.info(f"""
                **Most Improved:** {most_improved}
                Change: {improvement:.2f}%
                """)
    
    with col2:
        # Highest poverty
        worst_country_idx = latest_data['value'].idxmax()
        worst_country = latest_data.loc[worst_country_idx, 'country']
        worst_value = latest_data.loc[worst_country_idx, 'value']
        
        st.warning(f"""
        **Highest Poverty Rate:** {worst_country}  
        Rate: {worst_value:.2f}%
        """)
        
        # Overall trend
        overall_trend = global_data.groupby('year')['value'].mean()
        trend_change = overall_trend.iloc[-1] - overall_trend.iloc[0]
        
        st.info(f"""
        **Overall Trend:** {'Decreasing' if trend_change < 0 else 'Increasing'}  
        Change: {trend_change:+.2f} percentage points
        """)

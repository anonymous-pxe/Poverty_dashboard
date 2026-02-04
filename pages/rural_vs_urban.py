"""
Rural vs Urban page - Comparison of poverty rates by area type.
"""

import streamlit as st
from data.data_loader import load_india_data, load_rural_urban_comparison
from components.filters import render_year_selector, render_comparison_filters
from components.metrics import render_comparison_metrics
from components.tables import render_styled_table
from utils.visualization import create_bar_chart, create_box_plot, create_scatter_plot
import config


def render_rural_vs_urban_page():
    """Render the rural vs urban comparison page."""
    st.title("🏘️ Rural vs Urban Poverty Comparison")
    st.markdown("### Analyzing poverty disparities between rural and urban areas")
    
    # Filters
    st.markdown("---")
    selected_year = render_year_selector("Select Year for Comparison")
    
    # Load comparison data
    try:
        with st.spinner("Loading comparison data..."):
            comparison_data = load_rural_urban_comparison(year=selected_year)
            
            # Also load time series data
            rural_data = load_india_data(area_type='Rural', start_year=2010, end_year=2023)
            urban_data = load_india_data(area_type='Urban', start_year=2010, end_year=2023)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    if comparison_data.empty:
        st.warning("No data available for the selected year.")
        return
    
    # Summary metrics
    st.markdown("---")
    st.subheader(f"📊 Overview - {selected_year}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_rural = comparison_data['rural_poverty'].mean()
        st.metric(
            "Avg Rural Poverty",
            f"{avg_rural:.2f}%",
            help="Average poverty rate in rural areas"
        )
    
    with col2:
        avg_urban = comparison_data['urban_poverty'].mean()
        st.metric(
            "Avg Urban Poverty",
            f"{avg_urban:.2f}%",
            help="Average poverty rate in urban areas"
        )
    
    with col3:
        gap = avg_rural - avg_urban
        st.metric(
            "Rural-Urban Gap",
            f"{gap:.2f}%",
            delta=f"{gap:.2f}%",
            delta_color="inverse",
            help="Difference between rural and urban poverty rates"
        )
    
    # Visualization tabs
    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 State Comparison", 
        "📈 Time Trends", 
        "📉 Distribution", 
        "📋 Data Table"
    ])
    
    with tab1:
        st.subheader("State-wise Rural vs Urban Poverty Rates")
        
        # Prepare data for visualization
        import pandas as pd
        plot_data = pd.melt(
            comparison_data,
            id_vars=['state'],
            value_vars=['rural_poverty', 'urban_poverty'],
            var_name='Area Type',
            value_name='Poverty Rate'
        )
        plot_data['Area Type'] = plot_data['Area Type'].map({
            'rural_poverty': 'Rural',
            'urban_poverty': 'Urban'
        })
        
        # Grouped bar chart
        fig = create_bar_chart(
            df=plot_data,
            x_col='state',
            y_col='Poverty Rate',
            color_col='Area Type',
            title=f'Rural vs Urban Poverty by State ({selected_year})',
            barmode='group'
        )
        fig.update_xaxis(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Gap analysis
        st.markdown("---")
        st.subheader("Rural-Urban Gap Analysis")
        
        # Sort by gap
        gap_data = comparison_data.sort_values('difference', ascending=False).head(10)
        
        fig_gap = create_bar_chart(
            df=gap_data,
            x_col='state',
            y_col='difference',
            title='Top 10 States with Largest Rural-Urban Gap',
            orientation='v'
        )
        fig_gap.update_xaxis(tickangle=-45)
        st.plotly_chart(fig_gap, use_container_width=True)
    
    with tab2:
        st.subheader("Poverty Trends Over Time")
        
        # Select states for trend analysis
        selected_states = st.multiselect(
            "Select States to Compare",
            options=config.INDIAN_STATES,
            default=config.INDIAN_STATES[:3]
        )
        
        if selected_states:
            # Filter data
            rural_trend = rural_data[rural_data['state'].isin(selected_states)]
            urban_trend = urban_data[urban_data['state'].isin(selected_states)]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Rural Poverty Trends**")
                fig_rural = create_line_chart(
                    df=rural_trend,
                    x_col='year',
                    y_col='poverty_rate',
                    color_col='state',
                    title='Rural Poverty Trends',
                    x_label='Year',
                    y_label='Poverty Rate (%)'
                )
                st.plotly_chart(fig_rural, use_container_width=True)
            
            with col2:
                st.markdown("**Urban Poverty Trends**")
                fig_urban = create_line_chart(
                    df=urban_trend,
                    x_col='year',
                    y_col='poverty_rate',
                    color_col='state',
                    title='Urban Poverty Trends',
                    x_label='Year',
                    y_label='Poverty Rate (%)'
                )
                st.plotly_chart(fig_urban, use_container_width=True)
        else:
            st.info("Please select at least one state to view trends.")
    
    with tab3:
        st.subheader("Distribution Analysis")
        
        # Box plots for distribution comparison
        import pandas as pd
        box_data = pd.concat([
            rural_data[rural_data['year'] == selected_year][['poverty_rate']].assign(Area='Rural'),
            urban_data[urban_data['year'] == selected_year][['poverty_rate']].assign(Area='Urban')
        ])
        
        fig_box = create_box_plot(
            df=box_data,
            x_col='Area',
            y_col='poverty_rate',
            title=f'Poverty Rate Distribution - Rural vs Urban ({selected_year})'
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
        # Scatter plot
        st.markdown("---")
        st.subheader("Rural vs Urban Scatter Plot")
        
        fig_scatter = create_scatter_plot(
            df=comparison_data,
            x_col='rural_poverty',
            y_col='urban_poverty',
            title=f'Rural vs Urban Poverty Correlation ({selected_year})',
            trendline='ols'
        )
        # Add diagonal line for reference
        import plotly.graph_objects as go
        max_val = max(comparison_data['rural_poverty'].max(), comparison_data['urban_poverty'].max())
        fig_scatter.add_trace(
            go.Scatter(
                x=[0, max_val],
                y=[0, max_val],
                mode='lines',
                name='Equal Line',
                line=dict(dash='dash', color='gray')
            )
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Statistical test
        st.markdown("---")
        st.subheader("Statistical Comparison")
        
        from utils.stats import perform_hypothesis_test
        test_result = perform_hypothesis_test(
            group1=comparison_data['rural_poverty'],
            group2=comparison_data['urban_poverty'],
            test_type='t-test'
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Test Statistic", f"{test_result['statistic']:.4f}")
            st.metric("P-Value", f"{test_result['p_value']:.6f}")
        with col2:
            st.metric("Result", test_result['significance'])
            if test_result['p_value'] < 0.05:
                st.success("Rural and urban poverty rates are significantly different.")
            else:
                st.info("No significant difference found between rural and urban poverty rates.")
    
    with tab4:
        st.subheader("Complete Comparison Data")
        
        # Display full comparison table
        display_data = comparison_data.round(2)
        render_styled_table(
            df=display_data,
            title=f"Rural vs Urban Poverty Comparison ({selected_year})"
        )
        
        # Download option
        csv = display_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Comparison Data",
            data=csv,
            file_name=f"rural_urban_comparison_{selected_year}.csv",
            mime="text/csv"
        )
    
    # Key Insights
    st.markdown("---")
    st.subheader("💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Largest gap
        max_gap_idx = comparison_data['difference'].idxmax()
        max_gap_state = comparison_data.loc[max_gap_idx, 'state']
        max_gap_value = comparison_data.loc[max_gap_idx, 'difference']
        
        st.warning(f"""
        **Largest Rural-Urban Gap:** {max_gap_state}  
        Gap: {max_gap_value:.2f} percentage points
        """)
        
        # Smallest gap
        min_gap_idx = comparison_data['difference'].idxmin()
        min_gap_state = comparison_data.loc[min_gap_idx, 'state']
        min_gap_value = comparison_data.loc[min_gap_idx, 'difference']
        
        st.success(f"""
        **Smallest Rural-Urban Gap:** {min_gap_state}  
        Gap: {min_gap_value:.2f} percentage points
        """)
    
    with col2:
        # States where urban > rural (unusual)
        urban_higher = comparison_data[comparison_data['difference'] < 0]
        
        if not urban_higher.empty:
            st.info(f"""
            **Urban Poverty Higher than Rural:**  
            {len(urban_higher)} state(s) show this pattern
            """)
        
        # Average ratio
        avg_ratio = comparison_data['ratio'].mean()
        st.info(f"""
        **Average Rural/Urban Ratio:** {avg_ratio:.2f}x  
        Rural poverty is on average {avg_ratio:.2f} times urban poverty
        """)

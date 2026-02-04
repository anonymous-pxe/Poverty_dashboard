"""
Analysis page - Statistical analysis with correlation, regression, and summary stats.
"""

import streamlit as st
from data.data_loader import load_india_data
from components.filters import render_filters
from components.tables import render_styled_table, render_correlation_table
from utils.stats import (
    calculate_summary_statistics,
    calculate_correlation,
    perform_regression,
    calculate_trend
)
from utils.visualization import (
    create_heatmap,
    create_scatter_plot,
    create_line_chart,
    create_histogram
)
import config


def render_analysis_page():
    """Render the statistical analysis page."""
    st.title("📈 Statistical Analysis")
    st.markdown("### Advanced statistical analysis and correlations")
    
    # Filters
    filters = render_filters(
        show_year=True,
        show_state=False,
        show_country=False,
        show_area=True,
        show_indicator=False
    )
    
    year_range = filters.get('year_range', (2010, 2023))
    area_type = filters.get('area_type', 'Total')
    
    # Load data
    try:
        with st.spinner("Loading data..."):
            data = load_india_data(
                area_type=area_type,
                start_year=year_range[0],
                end_year=year_range[1]
            )
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    if data.empty:
        st.warning("No data available for selected filters.")
        return
    
    # Analysis tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Summary Statistics",
        "🔗 Correlation Analysis",
        "📉 Regression Analysis",
        "📈 Trend Analysis"
    ])
    
    with tab1:
        st.subheader("Descriptive Statistics")
        
        # Select columns for analysis
        numeric_cols = ['poverty_rate', 'literacy_rate', 'unemployment_rate', 
                       'per_capita_income', 'mpi']
        
        # Calculate summary statistics
        summary_stats = calculate_summary_statistics(data, columns=numeric_cols)
        
        render_styled_table(
            df=summary_stats,
            title="Summary Statistics for All Indicators"
        )
        
        st.markdown("---")
        
        # Distribution by state
        st.subheader("State-wise Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_indicator = st.selectbox(
                "Select Indicator",
                options=numeric_cols,
                format_func=lambda x: x.replace('_', ' ').title()
            )
        
        with col2:
            selected_year = st.selectbox(
                "Select Year",
                options=sorted(data['year'].unique(), reverse=True)
            )
        
        year_data = data[data['year'] == selected_year]
        
        # Top and bottom performers
        from components.tables import render_top_bottom_table
        render_top_bottom_table(
            df=year_data,
            value_col=selected_indicator,
            label_col='state',
            n=5
        )
        
        # Distribution visualization
        st.markdown("---")
        from utils.visualization import create_histogram
        fig_hist = create_histogram(
            df=year_data,
            x_col=selected_indicator,
            title=f'Distribution of {selected_indicator.replace("_", " ").title()} ({selected_year})'
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with tab2:
        st.subheader("Correlation Analysis")
        
        st.markdown("""
        Correlation analysis helps identify relationships between different poverty indicators.
        Values range from -1 (perfect negative correlation) to +1 (perfect positive correlation).
        """)
        
        # Select correlation method
        corr_method = st.selectbox(
            "Correlation Method",
            options=['pearson', 'spearman', 'kendall'],
            format_func=lambda x: x.capitalize()
        )
        
        # Calculate correlation
        corr_matrix = calculate_correlation(data, columns=numeric_cols, method=corr_method)
        
        # Heatmap
        fig_heatmap = create_heatmap(
            df=corr_matrix,
            title=f'{corr_method.capitalize()} Correlation Matrix'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Correlation table
        st.markdown("---")
        st.subheader("Correlation Values")
        render_correlation_table(data, method=corr_method)
        
        # Strong correlations
        st.markdown("---")
        st.subheader("Strong Correlations")
        
        # Find strong correlations (exclude diagonal)
        import numpy as np
        import pandas as pd
        
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append({
                    'Variable 1': corr_matrix.columns[i],
                    'Variable 2': corr_matrix.columns[j],
                    'Correlation': corr_matrix.iloc[i, j]
                })
        
        corr_df = pd.DataFrame(corr_pairs)
        corr_df['Abs_Correlation'] = corr_df['Correlation'].abs()
        strong_corr = corr_df[corr_df['Abs_Correlation'] > 0.5].sort_values(
            'Abs_Correlation', ascending=False
        )
        
        if not strong_corr.empty:
            render_styled_table(strong_corr[['Variable 1', 'Variable 2', 'Correlation']])
        else:
            st.info("No strong correlations (|r| > 0.5) found.")
    
    with tab3:
        st.subheader("Regression Analysis")
        
        st.markdown("""
        Regression analysis examines how independent variables predict a dependent variable.
        """)
        
        # Select variables for regression
        col1, col2 = st.columns(2)
        
        with col1:
            dependent_var = st.selectbox(
                "Dependent Variable (Y)",
                options=numeric_cols,
                index=0,
                format_func=lambda x: x.replace('_', ' ').title()
            )
        
        with col2:
            independent_vars = st.multiselect(
                "Independent Variables (X)",
                options=[col for col in numeric_cols if col != dependent_var],
                default=[col for col in numeric_cols if col != dependent_var][:2],
                format_func=lambda x: x.replace('_', ' ').title()
            )
        
        if independent_vars:
            # Perform regression
            try:
                regression_result = perform_regression(
                    df=data,
                    x_cols=independent_vars,
                    y_col=dependent_var
                )
                
                # Display results
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("R² Score", f"{regression_result['r_squared']:.4f}")
                with col2:
                    st.metric("RMSE", f"{regression_result['rmse']:.4f}")
                with col3:
                    st.metric("MAE", f"{regression_result['mae']:.4f}")
                with col4:
                    st.metric("Intercept", f"{regression_result['intercept']:.4f}")
                
                st.markdown("---")
                st.subheader("Regression Coefficients")
                render_styled_table(regression_result['coefficients'])
                
                # Residual plot
                st.markdown("---")
                st.subheader("Residual Analysis")
                
                import pandas as pd
                residual_df = pd.DataFrame({
                    'Predicted': regression_result['predictions'],
                    'Residual': regression_result['residuals']
                })
                
                fig_residual = create_scatter_plot(
                    df=residual_df,
                    x_col='Predicted',
                    y_col='Residual',
                    title='Residual Plot'
                )
                st.plotly_chart(fig_residual, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error performing regression: {str(e)}")
        else:
            st.info("Please select at least one independent variable.")
    
    with tab4:
        st.subheader("Trend Analysis")
        
        st.markdown("""
        Analyze trends over time using linear regression.
        """)
        
        # Select variable and state
        col1, col2 = st.columns(2)
        
        with col1:
            trend_var = st.selectbox(
                "Select Variable",
                options=numeric_cols,
                format_func=lambda x: x.replace('_', ' ').title(),
                key='trend_var'
            )
        
        with col2:
            trend_states = st.multiselect(
                "Select States",
                options=data['state'].unique().tolist(),
                default=data['state'].unique().tolist()[:3]
            )
        
        if trend_states:
            # Calculate trends for each state
            trend_results = []
            
            for state in trend_states:
                state_data = data[data['state'] == state]
                trend = calculate_trend(
                    df=state_data,
                    time_col='year',
                    value_col=trend_var
                )
                trend['state'] = state
                trend_results.append(trend)
            
            import pandas as pd
            trend_df = pd.DataFrame(trend_results)
            
            # Display trend summary
            st.subheader("Trend Summary")
            display_cols = ['state', 'direction', 'slope', 'percent_change', 'r_squared']
            render_styled_table(trend_df[display_cols].round(4))
            
            # Visualize trends
            st.markdown("---")
            st.subheader("Trend Visualization")
            
            filtered_data = data[data['state'].isin(trend_states)]
            fig_trend = create_line_chart(
                df=filtered_data,
                x_col='year',
                y_col=trend_var,
                color_col='state',
                title=f'{trend_var.replace("_", " ").title()} Trends by State'
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
            # Insights
            st.markdown("---")
            st.subheader("Trend Insights")
            
            increasing = trend_df[trend_df['direction'] == 'Increasing']
            decreasing = trend_df[trend_df['direction'] == 'Decreasing']
            
            col1, col2 = st.columns(2)
            
            with col1:
                if not increasing.empty:
                    st.warning(f"""
                    **Increasing Trend:** {len(increasing)} state(s)  
                    Fastest increase: {increasing.loc[increasing['slope'].idxmax(), 'state']}
                    """)
                else:
                    st.success("No states showing increasing trend")
            
            with col2:
                if not decreasing.empty:
                    st.success(f"""
                    **Decreasing Trend:** {len(decreasing)} state(s)  
                    Fastest decrease: {decreasing.loc[decreasing['slope'].idxmin(), 'state']}
                    """)
                else:
                    st.info("No states showing decreasing trend")
        else:
            st.info("Please select at least one state for trend analysis.")

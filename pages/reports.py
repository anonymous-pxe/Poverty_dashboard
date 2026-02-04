"""
Reports page - PDF generation and data export functionality.
"""

import streamlit as st
from data.data_loader import load_india_data, load_global_data
from components.filters import render_filters
from utils.pdf_generator import (
    generate_pdf_report,
    export_dataframe_to_csv,
    export_dataframe_to_excel
)
from datetime import datetime
import config


def render_reports_page():
    """Render the reports and export page."""
    st.title("📄 Reports & Export")
    st.markdown("### Generate reports and export data")
    
    # Report type selection
    report_type = st.selectbox(
        "Select Report Type",
        options=["India State Report", "Global Report", "Custom Data Export"]
    )
    
    st.markdown("---")
    
    if report_type == "India State Report":
        render_india_report()
    elif report_type == "Global Report":
        render_global_report()
    else:
        render_custom_export()


def render_india_report():
    """Render India state report generation."""
    st.subheader("🇮🇳 India State Poverty Report")
    
    # Filters
    filters = render_filters(
        show_year=True,
        show_state=True,
        show_country=False,
        show_area=True,
        show_indicator=False
    )
    
    year_range = filters.get('year_range', (2010, 2023))
    states = filters.get('states', config.INDIAN_STATES[:5])
    area_type = filters.get('area_type', 'Total')
    
    if not states:
        st.warning("Please select at least one state.")
        return
    
    # Load data
    try:
        with st.spinner("Loading data..."):
            data = load_india_data(
                states=states,
                area_type=area_type,
                start_year=year_range[0],
                end_year=year_range[1]
            )
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    # Data preview
    st.subheader("📊 Data Preview")
    st.dataframe(data.head(10), use_container_width=True)
    
    st.markdown("---")
    
    # Export options
    st.subheader("💾 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export to CSV", use_container_width=True):
            try:
                filename = f"india_poverty_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                filepath = export_dataframe_to_csv(data, filename)
                st.success(f"CSV exported successfully!")
                
                # Provide download
                csv = data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=filename,
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error exporting CSV: {str(e)}")
    
    with col2:
        if st.button("📊 Export to Excel", use_container_width=True):
            try:
                filename = f"india_poverty_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                filepath = export_dataframe_to_excel(data, filename)
                st.success(f"Excel exported successfully!")
                
                # Note: For download, we'll convert again
                import io
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    data.to_excel(writer, index=False)
                
                st.download_button(
                    label="📥 Download Excel",
                    data=buffer.getvalue(),
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Error exporting Excel: {str(e)}")
    
    with col3:
        if st.button("📄 Generate PDF Report", use_container_width=True):
            try:
                # Prepare summary stats
                summary_stats = {
                    'Report Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Area Type': area_type,
                    'Year Range': f"{year_range[0]} - {year_range[1]}",
                    'States Included': len(states),
                    'Total Records': len(data),
                    'Average Poverty Rate': f"{data['poverty_rate'].mean():.2f}%"
                }
                
                # Prepare data tables
                latest_year = data['year'].max()
                latest_data = data[data['year'] == latest_year].head(20)
                
                data_tables = [
                    {
                        'title': f'Latest Year Data ({latest_year})',
                        'dataframe': latest_data[['state', 'poverty_rate', 'literacy_rate', 
                                                  'unemployment_rate', 'per_capita_income']]
                    }
                ]
                
                filename = f"india_poverty_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                filepath = generate_pdf_report(
                    filename=filename,
                    title="India State Poverty Report",
                    data_tables=data_tables,
                    summary_stats=summary_stats
                )
                
                st.success(f"PDF report generated successfully!")
                st.info(f"Report saved to: {filepath}")
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
    
    # Summary statistics
    st.markdown("---")
    st.subheader("📈 Summary Statistics")
    
    summary_cols = ['poverty_rate', 'literacy_rate', 'unemployment_rate', 'per_capita_income']
    summary = data[summary_cols].describe().T
    st.dataframe(summary.round(2), use_container_width=True)


def render_global_report():
    """Render global report generation."""
    st.subheader("🌍 Global Poverty Report")
    
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
        st.warning("Please select at least one country.")
        return
    
    # Load data
    try:
        with st.spinner("Loading global data..."):
            data = load_global_data(
                indicator=indicator,
                country_codes=countries,
                start_year=year_range[0],
                end_year=year_range[1]
            )
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return
    
    # Data preview
    st.subheader("📊 Data Preview")
    st.dataframe(data.head(10), use_container_width=True)
    
    st.markdown("---")
    
    # Export options
    st.subheader("💾 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"global_poverty_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        import pandas as pd
        import io
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            data.to_excel(writer, index=False)
        
        st.download_button(
            label="📊 Download as Excel",
            data=buffer.getvalue(),
            file_name=f"global_poverty_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )


def render_custom_export():
    """Render custom data export options."""
    st.subheader("🎯 Custom Data Export")
    
    st.markdown("""
    Select specific columns and filters to create a custom export of the poverty data.
    """)
    
    # Data source selection
    data_source = st.radio(
        "Select Data Source",
        options=["India State Data", "Global Data"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if data_source == "India State Data":
        # Filters for India data
        filters = render_filters(
            show_year=True,
            show_state=True,
            show_country=False,
            show_area=True,
            show_indicator=False
        )
        
        year_range = filters.get('year_range', (2010, 2023))
        states = filters.get('states', config.INDIAN_STATES[:5])
        area_type = filters.get('area_type', 'Total')
        
        if not states:
            st.warning("Please select at least one state.")
            return
        
        # Load data
        data = load_india_data(
            states=states,
            area_type=area_type,
            start_year=year_range[0],
            end_year=year_range[1]
        )
        
        # Column selection
        available_cols = data.columns.tolist()
        selected_cols = st.multiselect(
            "Select Columns to Export",
            options=available_cols,
            default=available_cols
        )
        
    else:
        # Filters for global data
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
            st.warning("Please select at least one country.")
            return
        
        # Load data
        data = load_global_data(
            indicator=indicator,
            country_codes=countries,
            start_year=year_range[0],
            end_year=year_range[1]
        )
        
        # Column selection
        available_cols = data.columns.tolist()
        selected_cols = st.multiselect(
            "Select Columns to Export",
            options=available_cols,
            default=available_cols
        )
    
    if not selected_cols:
        st.warning("Please select at least one column to export.")
        return
    
    # Filter data to selected columns
    export_data = data[selected_cols]
    
    # Preview
    st.subheader("📊 Export Preview")
    st.dataframe(export_data.head(20), use_container_width=True)
    st.info(f"Total rows to export: {len(export_data)}")
    
    # Export buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        csv = export_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"custom_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        import pandas as pd
        import io
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            export_data.to_excel(writer, index=False)
        
        st.download_button(
            label="📊 Download as Excel",
            data=buffer.getvalue(),
            file_name=f"custom_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

"""
Poverty Dashboard - Main Application Entry Point
A comprehensive data analysis and visualization platform for poverty indicators.
"""

import streamlit as st
import os
from pathlib import Path
import config
from components.sidebar import render_sidebar
from pages import (
    render_dashboard_page,
    render_global_trends_page,
    render_rural_vs_urban_page,
    render_analysis_page,
    render_visualization_page,
    render_reports_page,
    render_learn_more_page
)


# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT,
    initial_sidebar_state=config.SIDEBAR_STATE
)


def load_custom_css():
    """Load custom CSS styles with proper path resolution."""
    try:
        # Get absolute path to CSS file
        css_path = Path(__file__).parent / 'assets' / 'css' / 'style.css'
        with open(css_path, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        # If CSS file not found, use inline styles
        st.markdown("""
        <style>
        .main {
            background-color: #f8f9fa;
        }
        .stMetric {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #1f77b4;
        }
        </style>
        """, unsafe_allow_html=True)


def main():
    """Main application function with error handling."""
    # Load custom CSS
    load_custom_css()
    
    # Render sidebar and get selected page
    selected_page = render_sidebar()
    
    # Route to the appropriate page with error handling
    try:
        if selected_page == "Dashboard":
            render_dashboard_page()
        
        elif selected_page == "Global Trends":
            render_global_trends_page()
        
        elif selected_page == "Rural vs Urban":
            render_rural_vs_urban_page()
        
        elif selected_page == "Analysis":
            render_analysis_page()
        
        elif selected_page == "Visualization":
            render_visualization_page()
        
        elif selected_page == "Reports":
            render_reports_page()
        
        elif selected_page == "Learn More":
            render_learn_more_page()
        
        else:
            # Default to dashboard
            render_dashboard_page()
    
    except Exception as e:
        st.error(f"Error loading page '{selected_page}': {str(e)}")
        st.exception(e)
        st.info("Please try refreshing the page or selecting a different page from the sidebar.")


if __name__ == "__main__":
    main()

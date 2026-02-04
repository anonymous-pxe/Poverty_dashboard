"""
Sidebar component for navigation and global settings.
"""

import streamlit as st
import config


def render_sidebar():
    """
    Render the sidebar with navigation and filters.
    
    Returns:
        str: Selected page name
    """
    with st.sidebar:
        # Logo/Title
        st.title(config.APP_TITLE)
        st.markdown("---")
        
        # Navigation
        st.subheader("📍 Navigation")
        page = st.radio(
            "Go to:",
            options=list(config.PAGE_TITLES.keys()),
            format_func=lambda x: config.PAGE_TITLES[x],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # About section
        st.subheader("ℹ️ About")
        st.markdown("""
        This dashboard provides comprehensive insights into poverty metrics 
        across global and India-specific datasets.
        
        **Features:**
        - Global poverty trends
        - Rural vs Urban comparison
        - Statistical analysis
        - ML-based predictions
        - Report generation
        """)
        
        st.markdown("---")
        
        # Data source info
        with st.expander("📊 Data Sources"):
            st.markdown("""
            - **Global Data**: World Bank API
            - **India Data**: State-level poverty statistics
            - **Update Frequency**: Annual
            """)
        
        # Cache control
        with st.expander("🔄 Cache Control"):
            if st.button("Clear Cache"):
                st.cache_data.clear()
                st.success("Cache cleared!")
        
        # Footer
        st.markdown("---")
        st.caption(f"© 2024 Poverty Dashboard")
    
    return page

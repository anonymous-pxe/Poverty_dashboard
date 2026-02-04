"""
Sidebar component for navigation and global settings.
Simplified to use only native Streamlit components.
"""

import streamlit as st
import config


def render_sidebar():
    """
    Render the sidebar with navigation and filters.
    Simplified version using only Streamlit native components.
    
    Returns:
        str: Selected page name
    """
    with st.sidebar:
        # Logo/Title
        st.title("🌍 Poverty Dashboard")
        st.caption("Data-Driven Insights")
        st.markdown("---")
        
        # Navigation
        st.subheader("📍 Navigation")
        page = st.radio(
            "Go to:",
            options=list(config.PAGE_TITLES.keys()),
            format_func=lambda x: config.PAGE_TITLES[x],
            label_visibility="collapsed",
            key="page_navigation"
        )
        
        st.markdown("---")
        
        # About section
        with st.expander("ℹ️ About", expanded=False):
            st.write("""
            Comprehensive insights into poverty metrics across global 
            and India-specific datasets.
            
            **Features:**
            - Global poverty trends
            - Rural vs Urban comparison
            - Statistical analysis
            - ML-based predictions
            - Report generation
            """)
        
        # Data source info
        with st.expander("📊 Data Sources"):
            st.write("""
            **Global Data**: World Bank API  
            **India Data**: NDAP Platform (NITI Aayog)  
            **Update Frequency**: Annual
            """)
        
        # Cache control
        with st.expander("🔄 Cache Control"):
            if st.button("Clear Cache"):
                st.cache_data.clear()
                st.success("✅ Cache cleared!")
        
        # Live Data Status
        st.markdown("---")
        st.info("📈 **Live Data Enabled**")
        st.caption("Powered by World Bank & NDAP APIs")
        
        # Footer
        st.markdown("---")
        st.caption("© 2024 Poverty Dashboard")
        st.caption("Built with ❤️ using Streamlit")
    
    return page

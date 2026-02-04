"""
Sidebar component for navigation and global settings.
Enhanced with modern UI/UX design.
"""

import streamlit as st
import config


def render_sidebar():
    """
    Render the sidebar with navigation and filters.
    Enhanced with beautiful styling.
    
    Returns:
        str: Selected page name
    """
    with st.sidebar:
        # Logo/Title with gradient
        st.markdown("""
            <div style="text-align: center; padding: 1rem 0 2rem 0;">
                <h1 style="
                    font-size: 1.8rem;
                    font-weight: 700;
                    background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin: 0;
                ">🌍 Poverty Dashboard</h1>
                <p style="color: #ecf0f1; font-size: 0.875rem; margin-top: 0.5rem;">
                    Data-Driven Insights
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation with icons
        st.markdown("""
            <div style="margin-bottom: 1rem;">
                <h3 style="color: #ecf0f1; font-size: 0.875rem; font-weight: 600; 
                           text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;">
                    📍 Navigation
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        page = st.radio(
            "Go to:",
            options=list(config.PAGE_TITLES.keys()),
            format_func=lambda x: config.PAGE_TITLES[x],
            label_visibility="collapsed",
            key="page_navigation"
        )
        
        st.markdown("---")
        
        # About section with modern card
        st.markdown("""
            <div style="
                background: rgba(255, 255, 255, 0.1);
                padding: 1.25rem;
                border-radius: 12px;
                border-left: 4px solid #42a5f5;
                margin: 1rem 0;
            ">
                <h4 style="color: #42a5f5; margin: 0 0 0.75rem 0; font-size: 1rem;">
                    ℹ️ About
                </h4>
                <p style="color: #ecf0f1; font-size: 0.875rem; line-height: 1.6; margin: 0;">
                    Comprehensive insights into poverty metrics across global and India-specific datasets.
                </p>
                <div style="margin-top: 1rem;">
                    <div style="color: #42a5f5; font-size: 0.75rem; margin: 0.25rem 0;">
                        ✓ Global poverty trends
                    </div>
                    <div style="color: #42a5f5; font-size: 0.75rem; margin: 0.25rem 0;">
                        ✓ Rural vs Urban analysis
                    </div>
                    <div style="color: #42a5f5; font-size: 0.75rem; margin: 0.25rem 0;">
                        ✓ Statistical insights
                    </div>
                    <div style="color: #42a5f5; font-size: 0.75rem; margin: 0.25rem 0;">
                        ✓ ML predictions
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Data source info with expander
        with st.expander("📊 Data Sources", expanded=False):
            st.markdown("""
                <div style="font-size: 0.875rem; line-height: 1.6;">
                    <strong style="color: #42a5f5;">Global Data</strong><br/>
                    World Bank Open Data API<br/>
                    <br/>
                    <strong style="color: #42a5f5;">India Data</strong><br/>
                    NDAP Platform (NITI Aayog)<br/>
                    <br/>
                    <strong style="color: #42a5f5;">Update Frequency</strong><br/>
                    Annual updates
                </div>
            """, unsafe_allow_html=True)
        
        # Cache control with styled button
        with st.expander("🔄 Cache Control", expanded=False):
            if st.button("🗑️ Clear Cache", use_container_width=True):
                st.cache_data.clear()
                st.success("✅ Cache cleared successfully!")
        
        # Statistics badge
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <div style="
                    background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%);
                    color: white;
                    padding: 0.75rem;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 0.875rem;
                    margin-bottom: 0.5rem;
                ">
                    📈 Live Data Enabled
                </div>
                <div style="color: #95a5a6; font-size: 0.75rem;">
                    Powered by World Bank & NDAP APIs
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; color: #95a5a6; font-size: 0.75rem;">
                <div style="margin-bottom: 0.5rem;">© 2024 Poverty Dashboard</div>
                <div>Built with ❤️ using Streamlit</div>
            </div>
        """, unsafe_allow_html=True)
    
    return page

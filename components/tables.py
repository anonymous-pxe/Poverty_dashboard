"""
Table components for displaying styled data tables.
"""

import streamlit as st
import pandas as pd
from typing import Optional, List


def render_styled_table(df: pd.DataFrame,
                       title: Optional[str] = None,
                       height: Optional[int] = None,
                       use_container_width: bool = True):
    """
    Render a styled dataframe table.
    
    Args:
        df: DataFrame to display
        title: Optional table title
        height: Optional fixed height in pixels
        use_container_width: Whether to use full container width
    """
    if title:
        st.subheader(title)
    
    # Style the dataframe
    styled_df = df.style.format(precision=2, na_rep='N/A')
    
    # Highlight numeric columns
    numeric_cols = df.select_dtypes(include=['float64', 'float32', 'int64', 'int32']).columns
    if len(numeric_cols) > 0:
        styled_df = styled_df.background_gradient(
            subset=numeric_cols,
            cmap='RdYlGn_r',
            axis=0
        )
    
    st.dataframe(
        styled_df,
        height=height,
        use_container_width=use_container_width
    )


def render_summary_table(df: pd.DataFrame,
                        group_col: str,
                        value_cols: List[str],
                        agg_func: str = 'mean'):
    """
    Render a summary table with aggregations.
    
    Args:
        df: DataFrame to summarize
        group_col: Column to group by
        value_cols: Columns to aggregate
        agg_func: Aggregation function ('mean', 'sum', 'median', etc.)
    """
    summary = df.groupby(group_col)[value_cols].agg(agg_func).reset_index()
    
    # Round numeric columns
    numeric_cols = summary.select_dtypes(include=['float64', 'float32']).columns
    summary[numeric_cols] = summary[numeric_cols].round(2)
    
    render_styled_table(summary)


def render_comparison_table(df: pd.DataFrame,
                           index_col: str,
                           compare_cols: List[str],
                           title: Optional[str] = None):
    """
    Render a comparison table with highlighting.
    
    Args:
        df: DataFrame to display
        index_col: Column to use as index
        compare_cols: Columns to compare
        title: Optional table title
    """
    if title:
        st.subheader(title)
    
    # Set index
    display_df = df.set_index(index_col)[compare_cols]
    
    # Apply styling
    styled_df = display_df.style.highlight_max(
        axis=0,
        color='lightgreen'
    ).highlight_min(
        axis=0,
        color='lightcoral'
    ).format(precision=2)
    
    st.dataframe(styled_df, use_container_width=True)


def render_pivot_table(df: pd.DataFrame,
                      index: str,
                      columns: str,
                      values: str,
                      aggfunc: str = 'mean',
                      title: Optional[str] = None):
    """
    Render a pivot table.
    
    Args:
        df: DataFrame to pivot
        index: Column for index
        columns: Column for columns
        values: Column for values
        aggfunc: Aggregation function
        title: Optional table title
    """
    if title:
        st.subheader(title)
    
    pivot = pd.pivot_table(
        df,
        index=index,
        columns=columns,
        values=values,
        aggfunc=aggfunc
    )
    
    # Round values
    pivot = pivot.round(2)
    
    # Style with color gradient
    styled_pivot = pivot.style.background_gradient(
        cmap='RdYlGn_r',
        axis=None
    ).format(precision=2)
    
    st.dataframe(styled_pivot, use_container_width=True)


def render_sortable_table(df: pd.DataFrame,
                         default_sort_col: Optional[str] = None,
                         ascending: bool = True):
    """
    Render a sortable table with column selection.
    
    Args:
        df: DataFrame to display
        default_sort_col: Default column to sort by
        ascending: Sort order
    """
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        sort_col = st.selectbox(
            "Sort by",
            options=df.columns.tolist(),
            index=df.columns.tolist().index(default_sort_col) if default_sort_col else 0
        )
    
    with col2:
        sort_order = st.radio("Order", ["Ascending", "Descending"], horizontal=True)
        ascending = (sort_order == "Ascending")
    
    with col3:
        show_rows = st.number_input("Rows to show", min_value=5, max_value=len(df), value=min(20, len(df)))
    
    # Sort and display
    sorted_df = df.sort_values(by=sort_col, ascending=ascending).head(int(show_rows))
    render_styled_table(sorted_df)


def render_downloadable_table(df: pd.DataFrame,
                              filename: str = "data.csv",
                              title: Optional[str] = None):
    """
    Render a table with download button.
    
    Args:
        df: DataFrame to display
        filename: Default filename for download
        title: Optional table title
    """
    if title:
        st.subheader(title)
    
    # Display table
    st.dataframe(df, use_container_width=True)
    
    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )


def render_correlation_table(df: pd.DataFrame, method: str = 'pearson'):
    """
    Render a correlation matrix table.
    
    Args:
        df: DataFrame with numeric columns
        method: Correlation method ('pearson', 'spearman', 'kendall')
    """
    st.subheader("Correlation Matrix")
    
    # Calculate correlation
    numeric_cols = df.select_dtypes(include=['float64', 'float32', 'int64', 'int32']).columns
    corr = df[numeric_cols].corr(method=method)
    
    # Style with diverging colormap
    styled_corr = corr.style.background_gradient(
        cmap='RdBu_r',
        vmin=-1,
        vmax=1
    ).format(precision=2)
    
    st.dataframe(styled_corr, use_container_width=True)


def render_top_bottom_table(df: pd.DataFrame,
                           value_col: str,
                           label_col: str,
                           n: int = 5):
    """
    Render top and bottom performers side by side.
    
    Args:
        df: DataFrame to analyze
        value_col: Column with values
        label_col: Column with labels
        n: Number of top/bottom items to show
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔝 Top Performers")
        top_df = df.nlargest(n, value_col)[[label_col, value_col]]
        top_df = top_df.reset_index(drop=True)
        top_df.index += 1
        st.dataframe(top_df, use_container_width=True)
    
    with col2:
        st.markdown("### 🔻 Bottom Performers")
        bottom_df = df.nsmallest(n, value_col)[[label_col, value_col]]
        bottom_df = bottom_df.reset_index(drop=True)
        bottom_df.index += 1
        st.dataframe(bottom_df, use_container_width=True)

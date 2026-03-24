"""Statistics Page - Charts and Metrics."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dashboard_utils.db_helper import get_statistics

st.set_page_config(page_title="Statistics", page_icon="📊", layout="wide")

st.title("📊 Statistics & Analytics")
st.markdown("Real-time insights from scraping operations")

# Fetch statistics
try:
    stats = get_statistics()

    # Key Metrics Row
    st.markdown("### 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Articles",
            value=stats["total_articles"],
            delta=None,
            help="Total articles in database",
        )

    with col2:
        st.metric(
            label="Domains",
            value=len(stats["by_source"]),
            delta=None,
            help="Number of unique domains",
        )

    with col3:
        st.metric(
            label="Average Quality",
            value=f"{stats['average_quality_score']:.2f}",
            delta=None,
            help="Average quality score (0.0-1.0)",
        )

    with col4:
        st.metric(
            label="Total Tags",
            value=stats["total_tags"],
            delta=None,
            help="Unique tags extracted",
        )

    st.markdown("---")

    # Charts Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Articles by Domain")

        # Prepare data
        domain_data = pd.DataFrame(
            [{"domain": k, "count": v} for k, v in stats["by_source"].items()]
        ).sort_values("count", ascending=False)

        # Bar chart
        fig = px.bar(
            domain_data,
            x="domain",
            y="count",
            title="Articles per Domain",
            labels={"domain": "Domain", "count": "Articles"},
            color="count",
            color_continuous_scale="Blues",
        )
        fig.update_layout(xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🥧 Source Distribution")

        # Pie chart
        fig = px.pie(
            domain_data,
            values="count",
            names="domain",
            title="Article Distribution by Source",
            hole=0.3,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Charts Row 2
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Top 10 Domains")

        top_10 = domain_data.head(10)

        fig = go.Figure(
            data=[
                go.Bar(
                    x=top_10["count"],
                    y=top_10["domain"],
                    orientation="h",
                    marker=dict(color=top_10["count"], colorscale="Viridis"),
                )
            ]
        )
        fig.update_layout(
            title="Top 10 Domains by Article Count",
            xaxis_title="Articles",
            yaxis_title="Domain",
            yaxis={"categoryorder": "total ascending"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 📊 Data Summary")

        # Summary table
        summary_data = {
            "Metric": [
                "Total Articles",
                "Total Domains",
                "Avg Articles/Domain",
                "Max Articles (Domain)",
                "Min Articles (Domain)",
                "Average Quality Score",
                "Total Tags",
            ],
            "Value": [
                stats["total_articles"],
                len(stats["by_source"]),
                f"{stats['total_articles'] / max(len(stats['by_source']), 1):.1f}",
                domain_data["count"].max() if len(domain_data) > 0 else 0,
                domain_data["count"].min() if len(domain_data) > 0 else 0,
                f"{stats['average_quality_score']:.2f}",
                stats["total_tags"],
            ],
        }

        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

        # Additional stats
        st.info(f"""
        **Data Quality:**
        - Average quality score: {stats['average_quality_score']:.2f}
        - Quality target: 0.40
        - Status: {'✅ Above target' if stats['average_quality_score'] >= 0.4 else '⚠️ Below target'}
        """)

    st.markdown("---")

    # Category breakdown if available
    if stats.get("by_category") and len(stats["by_category"]) > 1:
        st.markdown("### 📑 Articles by Category")

        category_data = pd.DataFrame(
            [{"category": k, "count": v} for k, v in stats["by_category"].items()]
        ).sort_values("count", ascending=False)

        fig = px.treemap(
            category_data,
            path=["category"],
            values="count",
            title="Article Distribution by Category",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Refresh button
    st.markdown("---")
    if st.button("🔄 Refresh Statistics"):
        st.rerun()

except Exception as e:
    st.error(f"Error loading statistics: {e}")
    st.info("""
    **No data available yet.**
    
    To see statistics:
    1. Go to 🚀 Scraper page
    2. Trigger domain discovery
    3. Start scraping
    4. Come back here to see results!
    """)

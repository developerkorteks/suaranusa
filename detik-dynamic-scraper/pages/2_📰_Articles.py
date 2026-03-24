"""Articles Page - Browse and Search."""

import streamlit as st
import pandas as pd
import requests
import sys
from pathlib import Path

# Add root to path for dashboard_utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from dashboard_utils.db_helper import search_articles, get_article

# Custom CSS for image gallery and lightbox
st.markdown(
    """
<style>
/* Image Gallery Styles */
.image-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
    margin: 20px 0;
}

.gallery-item {
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    cursor: pointer;
    transition: transform 0.2s;
}

.gallery-item:hover {
    transform: scale(1.05);
}

/* Media badges */
.media-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.8em;
    margin-right: 5px;
}

.badge-images {
    background-color: #e3f2fd;
    color: #1976d2;
}

.badge-videos {
    background-color: #fce4ec;
    color: #c2185b;
}
</style>
""",
    unsafe_allow_html=True,
)

import os

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


# Helper Functions
def scrape_article_detail(article_id: str) -> dict:
    """Scrape full article content via API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/articles/{article_id}/scrape-detail", timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


def get_article_detail(article_id: str) -> dict:
    """Get article details via API."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/articles/{article_id}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None


st.set_page_config(page_title="Articles", page_icon="📰", layout="wide")

st.title("📰 Article Browser")
st.markdown("Search and browse scraped articles")

# Search filters
st.markdown("### 🔍 Search & Filter")

col1, col2, col3 = st.columns(3)

with col1:
    query = st.text_input("🔎 Search query", placeholder="Enter keywords...")

with col2:
    source = st.text_input("🌐 Source domain", placeholder="e.g., news.detik.com")

with col3:
    limit = st.number_input(
        "📊 Results limit", min_value=10, max_value=500, value=50, step=10
    )

# Search button
search_btn = st.button("🔍 Search", type="primary")

st.markdown("---")

# Fetch and display articles
try:
    # Get articles
    articles = search_articles(
        query=query if query else None,
        source=source if source else None,
        category=None,
        limit=limit,
    )

    if articles:
        st.success(f"Found {len(articles)} articles")

        # Display mode selector
        view_mode = st.radio(
            "View mode:", ["📋 Table View", "📄 Card View"], horizontal=True
        )

        if view_mode == "📋 Table View":
            # Table view
            df = pd.DataFrame(
                [
                    {
                        "ID": a["id"],
                        "Title": (
                            a["title"][:80] + "..."
                            if a["title"] and len(a["title"]) > 80
                            else a["title"]
                        ),
                        "Source": a["source"],
                        "Quality": (
                            f"{a['quality_score']:.2f}"
                            if a.get("quality_score")
                            else "N/A"
                        ),
                        "Date": a.get("publish_date", "N/A"),
                    }
                    for a in articles
                ]
            )

            # Display table
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": st.column_config.TextColumn("ID", width="small"),
                    "Title": st.column_config.TextColumn("Title", width="large"),
                    "Source": st.column_config.TextColumn("Source", width="medium"),
                    "Quality": st.column_config.NumberColumn("Quality", format="%.2f"),
                    "Date": st.column_config.TextColumn("Date", width="medium"),
                },
            )

        else:
            # Card view
            for i, article in enumerate(articles):
                # Build expander title with media badges
                title = article.get("title", "No title")
                media_info = ""

                # Check for media in metadata
                metadata = article.get("metadata")
                if metadata:
                    try:
                        if isinstance(metadata, str):
                            import json

                            metadata = json.loads(metadata)

                        if isinstance(metadata, dict):
                            images_count = len(metadata.get("images", []))
                            videos_count = len(metadata.get("videos", []))

                            if images_count > 0:
                                media_info += f" 📸{images_count}"
                            if videos_count > 0:
                                media_info += f" 🎥{videos_count}"
                    except Exception as e:
                        # Silently handle metadata parsing errors
                        pass

                # Ensure media_info is string
                expander_title = f"**{title}**{media_info if media_info else ''}"

                with st.expander(expander_title):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.markdown(f"**ID:** `{article.get('id')}`")
                        st.markdown(f"**Source:** {article.get('source', 'Unknown')}")

                        if article.get("description"):
                            st.markdown(
                                f"**Description:** {article['description'][:200]}..."
                            )

                        if article.get("url"):
                            st.markdown(
                                f"**URL:** [{article['url']}]({article['url']})"
                            )

                        if article.get("tags"):
                            tags_str = ", ".join(article["tags"][:5])
                            st.markdown(f"**Tags:** {tags_str}")

                        # NEW: Content Preview
                        st.markdown("---")
                        if article.get("content"):
                            content_preview = article["content"][:200]
                            st.markdown(f"**Content Preview:**")
                            st.text(f"{content_preview}...")
                            st.caption(
                                f"✅ Has content ({len(article['content'])} characters)"
                            )
                        else:
                            st.caption(
                                "❌ No content yet - Use 'Scrape Content' button below"
                            )

                    with col2:
                        st.metric(
                            "Quality Score", f"{article.get('quality_score') or 0:.2f}"
                        )

                        if article.get("publish_date"):
                            st.caption(f"📅 {article['publish_date']}")

                        if article.get("author"):
                            st.caption(f"✍️ {article['author']}")

                    # NEW: Action Buttons and Detail View
                    st.markdown("---")
                    st.markdown("**Actions:**")

                    col_btn1, col_btn2, col_btn3 = st.columns(3)

                    with col_btn1:
                        # View full content button
                        if article.get("content"):
                            # Fix: Use unique key with index
                            if st.button(
                                "📖 View Full Content",
                                key=f"view_{article.get('id', '')}_{i}",
                                use_container_width=True,
                            ):
                                st.session_state[f"show_full_{article['id']}"] = True

                    with col_btn2:
                        # Scrape content button
                        # Fix: Use unique key with index to avoid duplicate keys when id is None
                        scrape_btn = st.button(
                            "🔍 Scrape Content",
                            key=f"scrape_{article.get('id', '')}_{i}",
                            type=(
                                "primary" if not article.get("content") else "secondary"
                            ),
                            use_container_width=True,
                        )

                        if scrape_btn:
                            with st.spinner(f"Scraping article {article['id']}..."):
                                result = scrape_article_detail(article["id"])

                                if result.get("success"):
                                    st.success(
                                        f"✅ Successfully scraped {result.get('content_length', 0)} characters!"
                                    )
                                    st.info(
                                        "Refresh the page to see the updated content."
                                    )
                                else:
                                    st.error(
                                        f"❌ Failed to scrape: {result.get('error', 'Unknown error')}"
                                    )

                    with col_btn3:
                        # Refresh article data button
                        if st.button(
                            "🔄 Refresh",
                            key=f"refresh_{article.get('id', '')}_{i}",
                            use_container_width=True,
                        ):
                            st.rerun()

                    # NEW: Full Content Display (expandable)
                    if st.session_state.get(
                        f"show_full_{article['id']}", False
                    ) and article.get("content"):
                        st.markdown("---")
                        st.markdown("### 📄 Full Article Content")

                        # Display full content in a nice box
                        st.text_area(
                            "Content",
                            value=article["content"],
                            height=400,
                            key=f"content_{article.get('id', '')}_{i}",
                            disabled=True,
                        )

                        # NEW: Display media if available
                        metadata = article.get("metadata")
                        if metadata:
                            try:
                                # Parse metadata if it's a string
                                if isinstance(metadata, str):
                                    import json

                                    metadata = json.loads(metadata)

                                # Display images
                                images = metadata.get("images", [])
                                if images:
                                    st.markdown("---")
                                    st.markdown("### 📸 Images")

                                    # Show main image first
                                    main_images = [
                                        img
                                        for img in images
                                        if img.get("type") == "main"
                                    ]
                                    body_images = [
                                        img
                                        for img in images
                                        if img.get("type") == "body"
                                    ]

                                    if main_images:
                                        st.markdown("**Main Image:**")
                                        for img in main_images:
                                            st.image(
                                                img["url"],
                                                caption=img.get("alt", "Image"),
                                                use_container_width=True,
                                            )

                                    if body_images:
                                        st.markdown("**Article Images:**")
                                        # Display in columns if multiple
                                        if len(body_images) > 1:
                                            cols = st.columns(min(len(body_images), 3))
                                            for idx, img in enumerate(body_images):
                                                with cols[idx % 3]:
                                                    st.image(
                                                        img["url"],
                                                        caption=img.get(
                                                            "alt", f"Image {idx+1}"
                                                        ),
                                                        use_container_width=True,
                                                    )
                                        else:
                                            for img in body_images:
                                                st.image(
                                                    img["url"],
                                                    caption=img.get("alt", "Image"),
                                                    use_container_width=True,
                                                )

                                # Display videos
                                videos = metadata.get("videos", [])
                                if videos:
                                    st.markdown("---")
                                    st.markdown("### 🎥 Videos")

                                    for vid in videos:
                                        st.markdown(f"**{vid.get('title', 'Video')}**")

                                        # Embed video iframe
                                        video_url = vid.get("url", "")
                                        if video_url:
                                            # Create responsive iframe
                                            st.markdown(
                                                f"""
                                            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; background: #000;">
                                                <iframe src="{video_url}" 
                                                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
                                                        frameborder="0" 
                                                        allowfullscreen>
                                                </iframe>
                                            </div>
                                            """,
                                                unsafe_allow_html=True,
                                            )

                                            # Show video link
                                            st.caption(
                                                f"🔗 [{vid.get('platform', 'Video')}]({video_url})"
                                            )

                                        st.markdown("")  # Spacing

                            except Exception as e:
                                st.warning(f"Could not load media: {e}")

                        # Hide button
                        st.markdown("---")
                        if st.button(
                            "Hide Content", key=f"hide_{article.get('id', '')}_{i}"
                        ):
                            st.session_state[f"show_full_{article.get('id', '')}"] = (
                                False
                            )
                            st.rerun()

        # Pagination info
        st.markdown("---")
        st.info(f"Showing {len(articles)} articles. Use filters to refine results.")

    else:
        st.warning(
            "No articles found. Try different search criteria or start scraping!"
        )

        st.info("""
        **Tips:**
        - Leave search empty to show all articles
        - Use source filter to find articles from specific domain
        - Increase limit to see more results
        """)

except Exception as e:
    st.error(f"Error loading articles: {e}")
    st.info("""
    **No data available yet.**
    
    To see articles:
    1. Go to 🚀 Scraper page
    2. Trigger scraping
    3. Come back here to browse!
    """)

# Quick stats sidebar
with st.sidebar:
    st.markdown("### 📊 Quick Stats")
    try:
        from dashboard_utils.db_helper import get_statistics

        stats = get_statistics()
        st.metric("Total Articles", stats["total_articles"])
        st.metric("Total Domains", len(stats["by_source"]))
    except:
        st.info("No stats available")

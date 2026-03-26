import sqlite3
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

# Force Absolute Path for VPS
DB_PATH = "/root/suaranusa/data/comprehensive_full_test.db"

if not os.path.exists(DB_PATH):
    # Fallback for local testing
    DB_PATH = "data/comprehensive_full_test.db"

def infer_category(url, source):
    # Synchronized with Django Hardcoded Buttons
    if "/tag/" in url: return "TOPIK KHUSUS"
    if "/internasional/" in url: return "INTERNASIONAL"
    if "/edu/" in url: return "TEKNOLOGI"
    if "/sepakbola/" in url or "sport.detik.com" in source: return "OLAHRAGA"
    if "/finance/" in url or "finance.detik.com" in source: return "EKONOMI"
    if "20.detik.com" in source or "/video-" in url.lower(): return "VIDEO"
    if "hot.detik.com" in source: return "HIBURAN"
    if "health.detik.com" in source: return "NEWS"
    if "inet.detik.com" in source: return "TEKNOLOGI"
    if "wolipop.detik.com" in source: return "GAYA HIDUP"
    if "oto.detik.com" in source: return "OTOMOTIF"
    if "travel.detik.com" in source: return "TRAVEL"
    if "/berita/" in url or "news.detik.com" in source: return "NASIONAL"
    return "WARTA UTAMA"

def fix_database():
    print(f"Connecting to {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, url, source, category FROM articles")
    rows = cursor.fetchall()
    print(f"Found {len(rows)} articles to check.")
    
    updated_count = 0
    for row in rows:
        article_id = row['id']
        url = row['url'] or ""
        source = row['source'] or ""
        
        # 1. Clean Source
        clean_source = source
        if "://" in source or source.startswith("www."):
            try:
                parsed = urlparse(source if "://" in source else f"https://{source}")
                clean_source = parsed.netloc.replace("www.", "") or source
            except:
                pass
        
        # 2. Infer Category
        new_category = infer_category(url, clean_source)
        
        # 3. Update if changed
        if clean_source != source or row['category'] != new_category:
            cursor.execute(
                "UPDATE articles SET source = ?, category = ? WHERE id = ?",
                (clean_source, new_category, article_id)
            )
            updated_count += 1
            
    conn.commit()
    conn.close()
    print(f"Successfully updated {updated_count} articles with NEW MAPPING.")

if __name__ == "__main__":
    fix_database()

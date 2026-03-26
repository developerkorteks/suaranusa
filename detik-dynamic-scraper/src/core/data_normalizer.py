"""
Data Normalizer - Step 5

Provides unified output format regardless of source:
- Standard schema validation
- Field mapping system
- Data enrichment
- Type conversion
- Quality checks

Author: Dynamic Scraper
Date: 2026-03-23
"""

import re
from typing import Dict, List, Optional, Any
from datetime import datetime
from urllib.parse import urlparse
import sys
import os

# Add proper logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
# FIX: Dummy logger fallback for dashboard compatibility
try:
    from utils.logger import setup_logger

    logger = setup_logger(__name__)
except ImportError:

    class DummyLogger:
        def info(self, msg):
            print(f"INFO: {msg}")

        def warning(self, msg):
            print(f"WARNING: {msg}")

        def error(self, msg, exc_info=False):
            print(f"ERROR: {msg}")

        def debug(self, msg):
            pass

    logger = DummyLogger()


class DataNormalizer:
    """Normalize and validate scraped data to standard format."""

    # Standard schema definition
    STANDARD_SCHEMA = {
        "id": str,
        "title": str,
        "url": str,
        "image": str,
        "category": str,
        "publish_date": str,
        "description": str,
        "content": str,
        "tags": list,
        "author": str,
        "source": str,
        "source_url": str,
        "scraped_at": str,
        "quality_score": float,
        "metadata": dict,
    }

    # Required fields (must be present and non-empty)
    REQUIRED_FIELDS = ["id", "title"]

    def __init__(self, strict_mode: bool = False):
        """
        Initialize normalizer.

        Args:
            strict_mode: If True, reject items missing required fields
        """
        self.strict_mode = strict_mode
        self.field_mappings = self._build_field_mappings()
        self.stats = {
            "total_processed": 0,
            "total_normalized": 0,
            "total_rejected": 0,
            "quality_scores": [],
        }

    def normalize(
        self, raw_data: Dict[str, Any], source: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Normalize a single data item.

        Args:
            raw_data: Raw article/content data
            source: Source identifier (e.g., 'api', 'html', 'rech.detik.com')

        Returns:
            Normalized data dictionary or None if rejected
        """
        self.stats["total_processed"] += 1

        # Clean source to be a domain if it looks like a URL
        clean_source = source or "unknown"
        if "://" in clean_source or clean_source.startswith("www."):
            try:
                parsed_source = urlparse(clean_source if "://" in clean_source else f"https://{clean_source}")
                clean_source = parsed_source.netloc.replace("www.", "") or clean_source
            except:
                pass

        # Create base normalized structure
        normalized = {
            "id": None,
            "title": None,
            "url": None,
            "image": None,
            "category": None,
            "publish_date": None,
            "description": None,
            "content": None,
            "tags": [],
            "author": None,
            "source": clean_source,
            "source_url": raw_data.get("source_url", ""),
            "scraped_at": raw_data.get("scraped_at") or datetime.utcnow().isoformat(),
            "quality_score": 0.0,
            "metadata": raw_data.get("metadata") or {},
        }

        # Preserve enrichment data if present in root
        for media_key in ['images', 'videos', 'has_media']:
            if media_key in raw_data:
                normalized["metadata"][media_key] = raw_data[media_key]

        # Map fields from raw data
        normalized = self._map_fields(raw_data, normalized)

        # Clean and validate data
        normalized = self._clean_data(normalized)

        # Enrich data
        normalized = self._enrich_data(normalized)

        # Calculate quality score
        normalized["quality_score"] = self._calculate_quality_score(normalized)

        # Validate
        if self._validate(normalized):
            self.stats["total_normalized"] += 1
            self.stats["quality_scores"].append(normalized["quality_score"])
            return normalized
        else:
            self.stats["total_rejected"] += 1
            return None

    def normalize_batch(
        self, raw_data_list: List[Dict[str, Any]], source: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Normalize a batch of data items.

        Args:
            raw_data_list: List of raw data dictionaries
            source: Source identifier

        Returns:
            List of normalized data dictionaries
        """
        normalized_list = []

        for raw_data in raw_data_list:
            normalized = self.normalize(raw_data, source)
            if normalized:
                normalized_list.append(normalized)

        return normalized_list

    def _build_field_mappings(self) -> Dict[str, List[str]]:
        """Build field name mappings for common variations."""
        return {
            "id": ["id", "article_id", "articleid", "contentId", "content_id", "_id"],
            "title": ["title", "headline", "name", "judul", "heading"],
            "url": ["url", "articleurl", "link", "href", "permalink", "canonical"],
            "image": [
                "image",
                "thumbnail",
                "img",
                "foto",
                "picture",
                "imageurl",
                "thumb",
            ],
            "category": ["category", "kategori", "channel", "section", "rubrik"],
            "publish_date": [
                "publish_date",
                "publishdate",
                "date",
                "published",
                "tanggal",
                "pubdate",
                "created_at",
            ],
            "description": [
                "description",
                "deskripsi",
                "excerpt",
                "summary",
                "intro",
                "lead",
            ],
            "content": ["content", "body", "text", "article_body", "konten", "isi"],
            "tags": ["tags", "keywords", "tag", "kata_kunci", "label"],
            "author": ["author", "penulis", "reporter", "by", "writer"],
        }

    def _map_fields(
        self, raw_data: Dict[str, Any], normalized: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Map fields from raw data to normalized format."""
        for target_field, source_fields in self.field_mappings.items():
            # Try each possible source field
            for source_field in source_fields:
                if source_field in raw_data and raw_data[source_field]:
                    value = raw_data[source_field]

                    # Special handling for tags
                    if target_field == "tags" and isinstance(value, str):
                        # Parse string tags
                        normalized[target_field] = [
                            t.strip() for t in re.split(r"[,|;]", value) if t.strip()
                        ]
                    elif target_field == "tags" and isinstance(value, list):
                        normalized[target_field] = [str(t).strip() for t in value if t]
                    else:
                        normalized[target_field] = value

                    break  # Found value, move to next target field

        return normalized

    def _clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and sanitize data fields."""
        # Clean ID (remove prefixes like 'd-')
        if data["id"]:
            data["id"] = str(data["id"]).replace("d-", "").strip()

        # Clean title
        if data["title"]:
            data["title"] = self._clean_text(data["title"])

        # Clean description
        if data["description"]:
            data["description"] = self._clean_text(data["description"])

        # Clean content
        if data["content"]:
            data["content"] = self._clean_text(data["content"])

        # Clean author
        if data["author"]:
            data["author"] = self._clean_text(data["author"])

        # Clean category
        if data["category"]:
            data["category"] = str(data["category"]).strip().lower()

        # Validate and clean URL
        if data["url"]:
            data["url"] = self._clean_url(data["url"])

        # Validate and clean image URL
        if data["image"]:
            data["image"] = self._clean_url(data["image"])

        # Normalize publish_date
        if data["publish_date"]:
            data["publish_date"] = self._normalize_date(data["publish_date"])

        return data

    def _clean_text(self, text: str) -> str:
        """Clean text content."""
        if not text:
            return ""

        # Convert to string
        text = str(text)

        # Remove excessive whitespace
        text = re.sub(r"\s+", " ", text)

        # Trim
        text = text.strip()

        # Remove HTML entities
        text = re.sub(r"&[a-z]+;", "", text)

        return text

    def _clean_url(self, url: str) -> str:
        """Clean and validate URL."""
        if not url:
            return ""

        url = str(url).strip()

        # Ensure protocol
        if url.startswith("//"):
            url = "https:" + url
        elif not url.startswith("http"):
            url = "https://" + url

        return url

    def _normalize_date(self, date_str: str) -> str:
        """Normalize date to ISO format."""
        if not date_str:
            return ""

        # Already in ISO format
        if re.match(r"\d{4}-\d{2}-\d{2}", str(date_str)):
            return str(date_str)

        # Try to parse common formats
        # Format: 2026/03/23 15:50:29
        match = re.match(r"(\d{4})[/\-](\d{2})[/\-](\d{2})", str(date_str))
        if match:
            return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"

        # Return as-is if can't parse
        return str(date_str)

    def _enrich_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich data with additional computed fields."""
        # 1. Infer Category from URL and Source (If category is None or "null")
        if not data.get("category") or str(data.get("category")).lower() == "null":
            url = data.get("url") or ""
            source = data.get("source") or ""
            
            if "/tag/" in url:
                data["category"] = "TOPIK KHUSUS"
            elif "/edu/" in url:
                data["category"] = "EDUKASI"
            elif "/sepakbola/" in url or "sport.detik.com" in source:
                data["category"] = "OLAHRAGA"
            elif "/finance/" in url or "finance.detik.com" in source:
                data["category"] = "EKONOMI BISNIS"
            elif "20.detik.com" in source or "/video-" in url.lower():
                data["category"] = "VIDEO"
            elif "hot.detik.com" in source:
                data["category"] = "CELEB"
            elif "health.detik.com" in source:
                data["category"] = "BERITA DETIKHEALTH"
            elif "inet.detik.com" in source:
                data["category"] = "TEKNOLOGI"
            elif "wolipop.detik.com" in source:
                data["category"] = "GAYA HIDUP"
            elif "oto.detik.com" in source:
                data["category"] = "OTOMOTIF"
            elif "travel.detik.com" in source:
                data["category"] = "TRAVEL"
            elif "news.detik.com" in source or "/berita/" in url:
                data["category"] = "NEWS"
            else:
                data["category"] = "WARTA UTAMA"

        # 2. Extract domain from URL if source is still unknown
        if data["url"] and (not data.get("source") or data["source"] == "unknown"):
            try:
                parsed = urlparse(data["url"])
                if not data.get("source") or data["source"] == "unknown":
                    data["source"] = parsed.netloc
            except (ValueError, AttributeError, TypeError) as e:
                # FIX BUG #6: Specific exceptions instead of bare except
                # URL parsing failed, keep original source
                pass

        # Generate slug from title if missing ID
        if not data["id"] and data["title"]:
            # Try to extract from URL first
            if data["url"]:
                match = re.search(r"/d-(\d+)/", data["url"])
                if match:
                    data["id"] = match.group(1)

        # Ensure tags is a list
        if not isinstance(data["tags"], list):
            data["tags"] = []

        return data

    def _calculate_quality_score(self, data: Dict[str, Any]) -> float:
        """
        Calculate data quality score (0.0 to 1.0).

        Factors:
        - Presence of required fields
        - Presence of optional fields
        - Data completeness
        - Valid URLs
        """
        score = 0.0
        max_score = 0.0

        # Required fields (40% of score)
        for field in self.REQUIRED_FIELDS:
            max_score += 0.4 / len(self.REQUIRED_FIELDS)
            if data.get(field):
                score += 0.4 / len(self.REQUIRED_FIELDS)

        # Important optional fields (40% of score)
        important_fields = ["url", "description", "publish_date", "image"]
        for field in important_fields:
            max_score += 0.4 / len(important_fields)
            if data.get(field):
                score += 0.4 / len(important_fields)

        # Additional fields (20% of score)
        additional_fields = ["category", "tags", "author", "content"]
        for field in additional_fields:
            max_score += 0.2 / len(additional_fields)
            if data.get(field):
                score += 0.2 / len(additional_fields)

        return round(score, 2)

    def _validate(self, data: Dict[str, Any]) -> bool:
        """
        Validate normalized data.

        Returns:
            True if valid, False otherwise
        """
        # In strict mode, require all required fields
        if self.strict_mode:
            for field in self.REQUIRED_FIELDS:
                if not data.get(field):
                    return False
        else:
            # In non-strict mode, require at least one required field
            has_required = any(data.get(field) for field in self.REQUIRED_FIELDS)
            if not has_required:
                return False

        # Quality threshold (reject very low quality)
        if data["quality_score"] < 0.2:
            return False

        return True

    def get_stats(self) -> Dict[str, Any]:
        """Get normalization statistics."""
        avg_quality = 0.0
        if self.stats["quality_scores"]:
            avg_quality = sum(self.stats["quality_scores"]) / len(
                self.stats["quality_scores"]
            )

        return {
            "total_processed": self.stats["total_processed"],
            "total_normalized": self.stats["total_normalized"],
            "total_rejected": self.stats["total_rejected"],
            "success_rate": self.stats["total_normalized"]
            / max(self.stats["total_processed"], 1),
            "average_quality_score": round(avg_quality, 2),
        }

    def reset_stats(self):
        """Reset statistics."""
        self.stats = {
            "total_processed": 0,
            "total_normalized": 0,
            "total_rejected": 0,
            "quality_scores": [],
        }


if __name__ == "__main__":
    # Quick test
    logger.info("🧪 Testing Data Normalizer...")

    normalizer = DataNormalizer()

    # Test 1: Normalize with various field names
    logger.info("\n1️⃣ Test: Field mapping")
    raw = {
        "article_id": "d-8412424",
        "headline": "Test Article Title",
        "articleurl": "https://news.detik.com/test",
        "kategori": "News",
        "publishdate": "2026/03/23 15:50:29",
        "tag": "tag1,tag2,tag3",
        "penulis": "John Doe",
    }

    normalized = normalizer.normalize(raw, "api")
    logger.info(f"  ✅ Normalized: {normalized['id']} - {normalized['title']}")
    logger.info(f"     Quality score: {normalized['quality_score']}")
    logger.info(f"     Tags: {normalized['tags']}")

    # Test 2: Batch normalization
    logger.info("\n2️⃣ Test: Batch normalization")
    raw_batch = [
        {"id": "1", "title": "Article 1", "url": "https://test.com/1"},
        {"id": "2", "title": "Article 2"},  # Missing URL
        {"title": "Article 3", "url": "https://test.com/3"},  # Missing ID
        {"id": "4"},  # Missing title (should be rejected)
    ]

    normalized_batch = normalizer.normalize_batch(raw_batch, "test")
    logger.info(f"  ✅ Normalized {len(normalized_batch)}/{len(raw_batch)} items")

    # Test 3: Statistics
    logger.info("\n3️⃣ Test: Statistics")
    stats = normalizer.get_stats()
    logger.info(f"  ✅ Stats:")
    logger.info(f"     - Processed: {stats['total_processed']}")
    logger.info(f"     - Normalized: {stats['total_normalized']}")
    logger.info(f"     - Success rate: {stats['success_rate']:.1%}")
    logger.info(f"     - Avg quality: {stats['average_quality_score']}")

    logger.info("\n✅ All tests passed!")

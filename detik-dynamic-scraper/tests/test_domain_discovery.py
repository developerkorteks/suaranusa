"""
Tests for Domain Discovery System - Step 1
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.domain_discovery import DomainDiscovery, discover_domains_sync


class TestDomainDiscovery:
    """Test suite for DomainDiscovery class."""

    def test_extract_subdomain_valid_url(self):
        """Test extracting subdomain from valid detik.com URL."""
        discovery = DomainDiscovery()

        # Test various URL formats
        assert (
            discovery._extract_subdomain("https://news.detik.com/berita")
            == "news.detik.com"
        )
        assert (
            discovery._extract_subdomain("https://finance.detik.com")
            == "finance.detik.com"
        )
        assert discovery._extract_subdomain("https://www.detik.com") == "www.detik.com"
        assert discovery._extract_subdomain("https://20.detik.com") == "20.detik.com"

    def test_extract_subdomain_with_path(self):
        """Test extracting subdomain from URL with path."""
        discovery = DomainDiscovery()

        url = "https://news.detik.com/berita/d-8412424/artikel-test"
        assert discovery._extract_subdomain(url) == "news.detik.com"

    def test_extract_subdomain_protocol_relative(self):
        """Test extracting subdomain from protocol-relative URL."""
        discovery = DomainDiscovery()

        url = "//cdn.detik.net.id/assets/js/script.js"
        result = discovery._extract_subdomain(url)
        # Should extract cdn.detik.net.id
        assert result is not None
        assert "detik" in result

    def test_extract_subdomain_relative_url(self):
        """Test that relative URLs return None."""
        discovery = DomainDiscovery()

        assert discovery._extract_subdomain("/berita/artikel") is None
        assert discovery._extract_subdomain("/assets/css/style.css") is None

    def test_extract_subdomain_non_detik(self):
        """Test that non-detik URLs return None."""
        discovery = DomainDiscovery()

        assert discovery._extract_subdomain("https://google.com") is None
        assert discovery._extract_subdomain("https://facebook.com") is None

    def test_discover_domains_returns_set(self):
        """Test that discover returns a set."""
        domains = discover_domains_sync()

        assert isinstance(domains, set)
        assert len(domains) > 0

    def test_discover_finds_known_domains(self):
        """Test that discovery finds known major domains."""
        domains = discover_domains_sync()

        # Should find at least some of these major domains
        expected_domains = [
            "www.detik.com",
            "news.detik.com",
            "finance.detik.com",
        ]

        found_count = sum(1 for d in expected_domains if d in domains)
        assert (
            found_count >= 2
        ), f"Should find at least 2 major domains, found {found_count}"

    def test_get_domains_by_category(self):
        """Test domain categorization."""
        discovery = DomainDiscovery()

        # Add some test domains
        discovery.discovered_domains = {
            "news.detik.com",
            "finance.detik.com",
            "rech.detik.com",
            "cdn.detik.net.id",
            "adsmart.detik.com",
        }

        categories = discovery.get_domains_by_category()

        assert isinstance(categories, dict)
        assert "content" in categories
        assert "api" in categories
        assert "cdn" in categories
        assert "services" in categories

        # Check categorization
        assert "news.detik.com" in categories["content"]
        assert "rech.detik.com" in categories["api"]
        assert "adsmart.detik.com" in categories["services"]

    def test_discovery_finds_minimum_domains(self):
        """Test that discovery finds at least 10 domains."""
        domains = discover_domains_sync()

        assert (
            len(domains) >= 10
        ), f"Should find at least 10 domains, found {len(domains)}"

        print(f"\n✅ Discovered {len(domains)} domains:")
        for domain in sorted(domains)[:20]:  # Print first 20
            print(f"  - {domain}")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])

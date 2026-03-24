import re

html = """[HTML content from user]"""

# Extract all unique domains/subdomains
domains = re.findall(r"https?://([a-z0-9\-\.]+\.detik\.[a-z\.]+)", html)
unique_domains = sorted(set(domains))

print("=" * 80)
print("ALL DETIK DOMAINS/SUBDOMAINS FOUND IN HTML:")
print("=" * 80)
for i, domain in enumerate(unique_domains, 1):
    print(f"{i:3d}. {domain}")

print(f"\nTotal unique domains: {len(unique_domains)}")

# Extract API endpoints
print("\n" + "=" * 80)
print("API ENDPOINTS DETECTED:")
print("=" * 80)

api_patterns = [
    r"https://([a-z0-9\-]+\.detik\.com)/([a-z\-]+)/([a-z\-]+)",
    r"https://([a-z0-9\-]+\.detik\.com)/api/",
    r"https://([a-z0-9\-]+\.detik\.com)/delivery/",
]

for pattern in api_patterns:
    apis = re.findall(pattern, html)
    for api in set(apis):
        if isinstance(api, tuple):
            print(f"  - {'/'.join(api)}")
        else:
            print(f"  - {api}")

# Extract tracking/analytics domains
print("\n" + "=" * 80)
print("TRACKING & ANALYTICS:")
print("=" * 80)
tracking = re.findall(
    r'https?://([^"\s<>]+(?:google|analytics|tag|gtm|doubleclick)[^"\s<>]*)', html
)
for t in set(tracking)[:20]:
    print(f"  - {t}")

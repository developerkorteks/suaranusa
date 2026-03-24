import re
import json

with open(
    "/home/korteks/Data/project/suaranusa.my.id/detik.com/htmlhome.md",
    "r",
    encoding="utf-8",
) as f:
    html = f.read()

# Find all articles
articles = re.findall(r"<article[^>]*>(.*?)</article>", html, re.DOTALL)

results = []
for art in articles:
    # Title and Link
    title_match = re.search(
        r'<h[23][^>]*class="[^"]*media__title[^"]*"[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
        art,
        re.DOTALL | re.IGNORECASE,
    )

    if title_match:
        link = title_match.group(1).strip()
        title = re.sub(r"<[^>]+>", "", title_match.group(2)).strip()
        title = title.replace("\n", " ").replace("\r", "")
        title = re.sub(r"\s+", " ", title)

        # Image
        img_match = re.search(r'<img[^>]*src="([^"]+)"', art, re.IGNORECASE)
        if not img_match:
            img_match = re.search(r'<img[^>]*data-src="([^"]+)"', art, re.IGNORECASE)
        img = img_match.group(1) if img_match else None

        # Category / Label
        label_match = re.search(
            r'class="[^"]*media__label[^"]*"[^>]*>(.*?)</div>',
            art,
            re.DOTALL | re.IGNORECASE,
        )
        if not label_match:
            label_match = re.search(
                r'class="[^"]*media__subtitle[^"]*"[^>]*>(.*?)</div>',
                art,
                re.DOTALL | re.IGNORECASE,
            )
        label = (
            re.sub(r"<[^>]+>", "", label_match.group(1)).strip()
            if label_match
            else None
        )

        # Date
        date_match = re.search(
            r'class="[^"]*media__date[^"]*"[^>]*>(.*?)</div>',
            art,
            re.DOTALL | re.IGNORECASE,
        )
        date = (
            re.sub(r"<[^>]+>", "", date_match.group(1)).strip() if date_match else None
        )

        results.append(
            {
                "title": title,
                "link": link,
                "image": img,
                "category": label,
                "date": date,
            }
        )
    else:
        # fallback for articles without media__title
        a_match = re.search(
            r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', art, re.DOTALL | re.IGNORECASE
        )
        if a_match:
            link = a_match.group(1).strip()
            title = re.sub(r"<[^>]+>", "", a_match.group(2)).strip()
            title = title.replace("\n", " ").replace("\r", "")
            title = re.sub(r"\s+", " ", title)

            results.append(
                {
                    "title": title,
                    "link": link,
                    "image": None,
                    "category": None,
                    "date": None,
                }
            )

with open(
    "/home/korteks/Data/project/suaranusa.my.id/detik.com/scraped_home.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print(f"Extracted {len(results)} articles.")

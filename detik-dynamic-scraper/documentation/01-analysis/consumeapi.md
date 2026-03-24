# Best Practice: API Consumption for Automated Production Frontend

This document outlines the professional standards and architectural patterns for consuming the Detik Dynamic Scraper API in a fully automated, production-grade frontend application.

## 1. Architectural Strategy

To achieve a seamless "news portal" experience without manual buttons, the frontend must implement a decoupling strategy between data presentation and data acquisition.

### Key Patterns:
- **JIT (Just-In-Time) Hydration:** Load article lists immediately; fetch full content and media only when the user navigates to the detail view.
- **Background Synchronization:** Trigger mass scraping via server-side CRON or background workers rather than user interactions.
- **Optimistic UI:** Show cached list data while silently validating freshness in the background.

---

## 2. Endpoint Implementation Standards

### Phase A: The Discovery Layer (Background Process)
The frontend or a dedicated middleware should maintain a fresh list of active domains.

**Endpoint:** `POST /api/discover-domains`
**Standard:** Run once every 24 hours. Store the resulting domain list in a global state or edge cache.

### Phase B: Automated Listing (Index Page)
Display articles automatically as they are scraped.

**Endpoint:** `POST /api/articles/search`
**Payload Example:**
```json
{
  "query": null,
  "source": "news.detik.com",
  "limit": 20,
  "offset": 0
}
```
**Best Practice:**
- Implement **Infinite Scroll** using the `offset` and `limit` parameters.
- Order by `scraped_at` or `publish_date` descendently to ensure the latest news appears at the top.

### Phase C: Detail View & Auto-Hydration
When a user clicks an article, the frontend must handle cases where full content is not yet available.

**Sequence:**
1. Call `GET /api/articles/{article_id}`.
2. Check if `content` is present and substantial.
3. If `content` is missing:
   - Display a skeleton loader.
   - Automatically call `POST /api/articles/{article_id}/scrape-detail`.
   - On success, re-fetch the article data and update the UI.

---

## 3. Media Rendering Best Practices

The API provides a structured `metadata` object containing images and videos.

### Image Handling:
- **Main Image:** Use the image object with `type: "main"`.
- **Body Gallery:** Render images with `type: "body"` in a grid or within the text flow based on their original position.
- **Lazy Loading:** Always use `loading="lazy"` for body images to maintain high performance.

### Video Integration:
- **Platform Detection:** Check the `platform` field (`20detik` or `youtube`).
- **Responsive Embeds:** Wrap the provided iframe URLs in a container with a `16:9` aspect ratio.
- **Fallback:** If the embed fails, use the provided platform link as a "Watch on..." button.

---

## 4. Performance & Reliability

### Rate Limiting and Caching:
- **Client-Side Cache:** Cache API responses for at least 5 minutes to prevent redundant network requests.
- **Error Boundaries:** If `scrape-detail` fails, fall back to the `description` provided in the list view to ensure the user still has something to read.

### Content Sanitization:
- The API returns raw text. The frontend should handle paragraph spacing (`

`) and avoid rendering raw HTML tags unless explicitly sanitized.

---

## 5. Automated Data Maintenance

For a production site, use the **Batch Update** capability to keep the database enriched with media without user intervention.

**Endpoint:** `POST /api/articles/batch-update-media`
**Payload:**
```json
{
  "limit": 50,
  "skip_existing": true,
  "rate_limit": 2.0
}
```
**Implementation:** This should be called by a backend service every hour to ensure all newly discovered articles are "fully hydrated" with images and videos before a user even clicks them.

---
*End of Best Practice Documentation*

from django.utils.dateparse import parse_datetime
from django.utils.timezone import now

def normalize_article(a):
    title = (a.get("title") or "").strip()
    url = a.get("url")

    if not title or not url:
        return None

    source = a.get("source") or {}

    return {
        "title": title,
        "url": url,
        "author": (a.get("author") or "").strip() or None,
        "description": a.get("description"),
        "content": a.get("content"),
        "published_at": parse_datetime(a.get("publishedAt")) or now(),
        "source_id": source.get("id") or source.get("name"),
        "url_to_image": a.get("urlToImage"),
    }

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now
from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import logging
import time
import json
from .models import Article, Source
from urllib.parse import urljoin
from bs4 import BeautifulSoup




logger = logging.getLogger(__name__)
API_KEY = "1d288bcfb535403ca6f3603c5fdb0ce4"


def home(request):
    saved_articles = Article.objects.order_by('-published_at')
    return render(request, "main/home.html", {
        'saved_articles': saved_articles,
        'fetched_articles': [],
        })

def fetch_articles(request):
    query = request.GET.get('q', '')  
    endpoint = request.GET.get('endpoint', 'everything')
    
    if endpoint == 'everything':
        url = f'https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}'
    else:
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    raw_articles = data.get('articles', [])
    
    articles = []
    for a in raw_articles:
        article = normalize_article(a)
        if article:
            articles.append(article)
    
    logger.info("Fetched %d articles", len(articles))
    
    return render(request, "main/fetched_articles.html", {
        'articles': articles,
    })
    
    
def normalize_article(a):
    title = (a.get('title') or '').strip()
    url_value = a.get('url')
    
    if not title or not url_value:
        return None

    published_at = parse_datetime(a.get('publishedAt')) or now()
    source = a.get("source") or {}

    return {
        'title': title,
        'url': url_value,
        'author': (a.get('author') or '').strip() or None,
        'description': a.get('description'),
        'content': a.get('content'),
        'published_at': published_at,
        'source_id': source.get('id') or source.get('name'),
        'url_to_image': a.get('urlToImage'),
    }


def save_article(request):
    data = json.loads(request.body)

    # prevent duplicates
    if Article.objects.filter(url=data['url']).exists():
        return JsonResponse({'status': 'exists'})

    Article.objects.create(
        title=data['title'],
        url=data['url'],
        author=data.get('author'),
        description=data.get('description'),
        content=data.get('content'),
        published_at=data['published_at'],
        source_id=data.get('source_id'),
        url_to_image=data.get('url_to_image'),
    )

    return JsonResponse({'status': 'saved'})

def my_articles(request):
    articles = Article.objects.order_by('-published_at')
    return render(request, "main/my_articles.html", { 'articles': articles })


def sources(request):
    sources = Source.objects.all()
    return render(request, "main/sources.html", {'sources': sources} )


@require_POST
def fetch_sources(request):
    url = "https://newsapi.org/v2/top-headlines/sources"
    params = {
        "apiKey": settings.NEWSAPI_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error("NewsAPI request failed: %s", e)
        return HttpResponse("NewsAPI request failed", status=502)

    data = response.json()
    sources = data.get("sources", [])

    allowed_categories = dict(Source.CATEGORY_CHOICES)

    created = 0
    updated = 0
    skipped = 0

    for s in sources:
        api_id = s.get("id")
        category = s.get("category")

        if not api_id or category not in allowed_categories:
            skipped += 1
            continue

        defaults = {
            "name": s.get("name", ""),
            "description": s.get("description", ""),
            "category": category,
            "language": s.get("language", ""),
            "country": s.get("country", ""),
            "url": s.get("url", ""),
        }

        obj, was_created = Source.objects.get_or_create(
            api_id=api_id,
            defaults=defaults,
        )

        if was_created:
            created += 1
            continue

        # Update existing records if changed
        dirty = False
        for field, value in defaults.items():
            if getattr(obj, field) != value:
                setattr(obj, field, value)
                dirty = True

        if dirty:
            obj.save(update_fields=defaults.keys())
            updated += 1

    logger.info(
        "NewsAPI sources sync complete: total=%d created=%d updated=%d skipped=%d",
        len(sources),
        created,
        updated,
        skipped,
    )

    return HttpResponse(
        f"Done. Created={created}, Updated={updated}, Skipped={skipped}"
    )
        
        
def extract_og_image(url):
    """Extract og:image from page HTML, fallback-safe."""
    try:
        response = requests.get(
            url, timeout=10, headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()
    except requests.RequestException:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    tag = soup.find("meta", property="og:image")
    if tag and tag.get("content"):
        return tag["content"]
    return None


@require_POST
def fetch_sources_images(request):
    sources = Source.objects.filter(url_to_image__isnull=True)
    total = sources.count()

    if total == 0:
        return HttpResponse("No sources need images.")

    updated = 0
    failed = 0
    skip_sources = {"CBC News"}  # fast lookup set

    logger.info("Fetching images for %d sources", total)

    for i, source in enumerate(sources, start=1):
        if source.name in skip_sources:
            logger.info("[%d/%d] %s skipped explicitly", i, total, source.name)
            continue

        try:
            image = extract_og_image(source.url)
            if image:
                source.url_to_image = urljoin(source.url, image)
                source.save(update_fields=["url_to_image"])
                updated += 1
                logger.info("[%d/%d] %s OK", i, total, source.name)
            else:
                failed += 1
                logger.warning("[%d/%d] %s no image found", i, total, source.name)

        except Exception as e:
            failed += 1
            logger.error("[%d/%d] %s failed: %s", i, total, source.name, e)
            time.sleep(1)  # polite backoff

    logger.info(
        "Image fetch complete: total=%d updated=%d failed=%d",
        total,
        updated,
        failed,
    )

    return HttpResponse(
        f"Done. Updated={updated}, Failed={failed}, Total={total}"
    )
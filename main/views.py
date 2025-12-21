from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now
from django.db import IntegrityError
import requests
import logging
from .models import Article

logger = logging.getLogger(__name__)


def home(request):
    articles = list(Article.objects.order_by('-published_at'))
    return render(request, "main/home.html", {'articles': articles})

def fetch_articles(request):
    API_KEY = "1d288bcfb535403ca6f3603c5fdb0ce4"
    query = request.GET.get('q', '')  
    endpoint = request.GET.get('endpoint', 'everything')
    if endpoint == 'everything':
        url = f'https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}'
    else:
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    articles = data.get('articles', [])

    logger.info(f"Fetched {len(articles)} articles")

    create_articles_bulk(articles)

    return redirect('home')

def create_articles_bulk(articles):
    articles_to_create = []
    
    for a in articles:
        title = (a.get('title') or '').strip()
        url_value = a.get('url')
        if not title or not url_value:
            continue
        
        # --- OPTIONAL FIELDS ---
        published_at = parse_datetime(a.get('publishedAt')) or now()
        source = a.get("source") or {}

        articles_to_create.append(
            Article(
                title=title,
                url=url_value,
                author=(a.get('author') or '').strip() or None,
                description=a.get('description'),
                content=a.get('content'),
                published_at=published_at,
                source_id=source.get('id') or source.get('name'),
                url_to_image=a.get('urlToImage'),
            )
        )    
            
    if articles_to_create:
        Article.objects.bulk_create(articles_to_create, ignore_conflicts=True)

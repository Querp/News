from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
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
    endpoint_param = request.GET.get('endpoint')

    articles = fetch_articles_from_api(query=query, endpoint_param=endpoint_param)

    return render(request, "main/fetched_articles.html", {
        'articles': articles,
    })

def fetch_articles_from_api(query='', endpoint_param=None):
    ENDPOINTS = {
        'everything': 'everything',
        'headlines': 'top-headlines',
    }

    query = (query or '').strip()

    # choose endpoint headlines if query is empty
    if endpoint_param == 'everything' and not query:
        endpoint = 'top-headlines'
    else:
        endpoint = ENDPOINTS.get(endpoint_param, 'everything')

    base_url = 'https://newsapi.org/v2/'
    params = {'apiKey': API_KEY}

    if endpoint == 'everything':
        url = base_url + 'everything'
        if query:
            params['q'] = query
    else:
        url = base_url + 'top-headlines'
        params['country'] = 'us'
        if query:
            params['q'] = query

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    raw_articles = data.get('articles', [])

    articles = []
    for a in raw_articles:
        article = normalize_article(a)
        if article:
            articles.append(article)

    logger.info("Fetched %d articles", len(articles))
    return articles

@csrf_exempt
@require_GET
def fetch_and_save_headlines(request):
    # optional secret key
    if request.GET.get('key') != 'F3H7K9X2L1Q8Z5M0':
        return JsonResponse({'error': 'unauthorized'}, status=401)

    articles = fetch_articles_from_api(endpoint_param='headlines')

    saved_count = 0
    for a in articles:
        # prevent duplicates
        obj, created = Article.objects.update_or_create(
            url=a['url'],
            defaults=a
        )
        if created:
            saved_count += 1

    return JsonResponse({'saved': saved_count})

# def fetch_articles(request):
#     ENDPOINTS = {
#         'everything': 'everything',
#         'headlines': 'top-headlines',
#     }
#     query = request.GET.get('q', '').strip()
#     endpoint_param = request.GET.get('endpoint')
    
#     # choose endpoint headlines if query is empty
#     if endpoint_param == 'everything' and not query:
#         endpoint = 'top-headlines'
#     else:
#         endpoint = ENDPOINTS.get(endpoint_param, 'everything')

    
#     base_url = 'https://newsapi.org/v2/'
#     params = {
#         'apiKey': API_KEY,
#     }
    
#     if endpoint == 'everything':
#         url = base_url + 'everything'
#         if query:
#             params['q'] = query
#     else:
#         url = base_url + 'top-headlines'
#         params['country'] = 'us'
#         if query:
#             params['q'] = query
        
#     response = requests.get(url, params=params, timeout=10)
#     response.raise_for_status()
    
#     data = response.json()
#     raw_articles = data.get('articles', [])
    
#     articles = []
#     for a in raw_articles:
#         article = normalize_article(a)
#         if article:
#             articles.append(article)
    
#     logger.info("Fetched %d articles", len(articles))
    
#     return render(request, "main/fetched_articles.html", {
#         'articles': articles,
#     })
    
    
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

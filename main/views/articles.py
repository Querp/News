from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import json

from ..models import Article
from ..services.newsapi import fetch_articles
from ..utils.normalization import normalize_article

def fetch_articles_view(request):
    query = request.GET.get("q", "")
    endpoint = request.GET.get("endpoint")

    raw = fetch_articles(
        api_key=settings.NEWSAPI_KEY,
        query=query,
        endpoint_param=endpoint,
    )

    articles = [
        a for a in (normalize_article(r) for r in raw)
        if a is not None
    ]

    return render(request, "main/fetched_articles.html", {
        "articles": articles
    })


def my_articles(request):
    articles = Article.objects.order_by("-published_at")
    return render(request, "main/my_articles.html", {
        "articles": articles
    })


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
        origin=Article.Origin.MANUAL,
    )

    return JsonResponse({'status': 'saved'})
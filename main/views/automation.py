from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.conf import settings
import logging

from ..models import Article
from ..services.newsapi import fetch_articles
from ..utils.normalization import normalize_article

logger = logging.getLogger(__name__)

@csrf_exempt
@require_GET
def fetch_and_save_headlines(request):
    if request.GET.get("key") != settings.FETCH_SECRET_KEY:
        return JsonResponse({"error": "unauthorized"}, status=401)

    try:
        raw = fetch_articles(
            api_key=settings.NEWS_API_KEY,
            endpoint_param="headlines",
        )
    except Exception:
        logger.exception("NewsAPI fetch failed")
        return JsonResponse({"error": "fetch_failed"}, status=500)

    saved = updated = 0

    for r in raw:
        article = normalize_article(r)
        if not article:
            continue

        obj, created = Article.objects.update_or_create(
            url=article["url"],
            defaults=article,
        )
        saved += created
        updated += not created

    return JsonResponse({
        "fetched": len(raw),
        "saved": saved,
        "updated": updated,
    })

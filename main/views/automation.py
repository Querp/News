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
    if request.GET.get("key") != settings.NEWSAPI_KEY:
        return JsonResponse({"error": "unauthorized"}, status=401)

    api_key = getattr(settings, "NEWS_API_KEY", None)
    if not api_key:
        logger.error("NEWS_API_KEY is missing in settings!")
        return JsonResponse({"error": "missing_api_key"}, status=500)

    try:
        raw = fetch_articles(
            api_key=api_key,
            endpoint_param="headlines",
        )
    except Exception as e:
        logger.exception("NewsAPI fetch failed: %s", e)
        return JsonResponse({
            "error": "fetch_failed",
            "detail": str(e),
        }, status=500)

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

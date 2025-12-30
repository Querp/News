from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.conf import settings
import logging
from threading import Thread

from ..models import Article
from ..services.newsapi import fetch_articles
from ..utils.normalization import normalize_article
from main.management.commands.extract_locations import Command


logger = logging.getLogger(__name__)

@csrf_exempt
@require_GET
def fetch_and_save_headlines(request):
    received_key = request.GET.get("key")
    logger.info("Fetch job key received: %s", received_key)
    
    if received_key != settings.FETCH_SECRET_KEY:
        logger.warning(
            "Unauthorized key: %s != %s", received_key, settings.FETCH_SECRET_KEY
        )
        return JsonResponse({"error": "unauthorized"}, status=401)

    
    
    if request.GET.get("key") != settings.FETCH_SECRET_KEY:
        return JsonResponse({"error": "unauthorized"}, status=401)

    api_key = getattr(settings, "NEWSAPI_KEY", None)
    if not api_key:
        logger.error("NEWSAPI_KEY is missing in settings!")
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

        obj, created = Article.objects.get_or_create(
            url=article["url"],
            defaults={
                **article,
                "origin": Article.Origin.AUTO,
            },
        )
        if not created:
            Article.objects.filter(pk=obj.pk).update(**article)
            
        saved += created
        updated += not created

    return JsonResponse({
        "fetched": len(raw),
        "saved": saved,
        "updated": updated,
    })

def extract_locations_view(request):
    key = request.GET.get("key")
    if key != settings.FETCH_SECRET_KEY:
        return HttpResponseForbidden("Invalid key")
    
    # Run extraction in background
    Thread(target=Command().handle).start()
    return JsonResponse({"status": "locations extraction started"})
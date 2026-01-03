from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from ..models import Article, Source, GlobalFetchPreferences, FetchRun
from ..services.newsapi import fetch_articles
from ..utils.normalization import normalize_article
from main.constants.newsapi import COUNTRY_LABELS, CATEGORIES





def settings_view(request):
    prefs, _ = GlobalFetchPreferences.objects.get_or_create(
        id=1,  # enforce singleton
        defaults={
            "countries": ["us", "nl"],
            "categories": [],
            "sources": [],
        },
    )

    countries = sorted(COUNTRY_LABELS.items(), key=lambda item: item[1])
    sources = Source.objects.all()
    fetchRuns = FetchRun.objects.all()

    return render(request, "main/settings.html", {
        "countries": countries,
        "categories": CATEGORIES,
        "sources": sources,
        "selected_countries": prefs.countries,
        "selected_categories": prefs.categories,
        "selected_sources": prefs.sources,
        "fetchRuns": fetchRuns,
    })
    
    
@require_POST
def update_preferences(request):
    """
    Expects JSON payload:
    {
        "type": "countries" | "categories" | "sources",
        "value": "...",
        "add": true|false
    }
    """
    prefs, _ = GlobalFetchPreferences.objects.get_or_create(
        id=1,
        defaults={"countries": [], "categories": [], "sources": []},
    )

    try:
        data = json.loads(request.body)
        type_ = data.get("type")
        value = data.get("value")
        add = data.get("add")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if type_ not in ("countries", "categories", "sources") or not value:
        return JsonResponse({"error": "Invalid type or value"}, status=400)

    current_list = getattr(prefs, type_)

    if add and value not in current_list:
        current_list.append(value)
    elif not add and value in current_list:
        current_list.remove(value)

    setattr(prefs, type_, current_list)
    prefs.save()

    return JsonResponse({"success": True, "type": type_, "value": value, "added": add})


def fetch_log_view(request):
    runs = FetchRun.objects.order_by("-started_at")[:100]
    return render(request, "fetch_log.html", {"runs": runs})
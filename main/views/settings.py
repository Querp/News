from django.shortcuts import render

from ..models import Article, Source, GlobalFetchPreferences
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

    return render(request, "main/settings.html", {
        "countries": countries,
        "categories": CATEGORIES,
        "sources": sources,
        "selected_countries": prefs.countries,
        "selected_categories": prefs.categories,
        "selected_sources": prefs.sources,
    })
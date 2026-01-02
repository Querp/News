from django.shortcuts import render

from ..models import Article, Source
from ..services.newsapi import fetch_articles
from ..utils.normalization import normalize_article

from main.constants.newsapi import COUNTRY_LABELS, CATEGORIES


def settings_view(request):
    countries = sorted(COUNTRY_LABELS.items(), key=lambda item: item[1])
    sources = Source.objects.all()

    return render(request, "main/settings.html", {
        "countries": countries, 
        "categories": CATEGORIES,
        "sources": sources,
    })
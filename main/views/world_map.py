from django.shortcuts import render
from django.db.models import Prefetch
from ..models import Article

def world_map_view(request):
    articles = Article.objects.order_by("-published_at").prefetch_related(
        Prefetch("locations", to_attr="all_locations")
    )
    
    for article in articles:
        for loc in article.all_locations:
            loc.top_percent = (90 - loc.latitude) / 180 * 100
            loc.left_percent = (loc.longitude + 180) / 360 * 100
    
    
    return render(request, "main/world_map.html", {
        "articles": articles
    })
from django.shortcuts import render
from ..models import Source

def sources(request):
    sources = Source.objects.all()
    return render(request, "main/sources.html", {
        "sources": sources
    })

from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now
from django.db import IntegrityError
import requests
from .models import Article


def home(request):
    articles = list(Article.objects.order_by('-published_at'))
    return render(request, "main/home.html", {'articles': articles})

def fetch_articles(request):
    API_KEY = "1d288bcfb535403ca6f3603c5fdb0ce4"
    query = request.GET.get('q', '')  
    endpoint = request.GET.get('endpoint', 'everything')
    if endpoint == 'everything':
        url = f'https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}'
    elif endpoint == 'headlines':
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'
    else:
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    articles = data.get('articles', [])

    print(len(articles), 'articles')
    # print(articles)
    

    for a in articles:
        # --- REQUIRED FIELDS ---
        title = (a.get('title') or '').strip()
        url_value = a.get('url')
        
        if not title or not url_value:
            continue
        
        published_at = parse_datetime(a.get('publishedAt')) or now()
        
        try:
            Article.objects.update_or_create(
                url=url_value,   # ✅ correct identity
                defaults={
                    'title': title,
                    'author': (a.get('author') or '').strip() or None,
                    'description': a.get('description'),
                    'content': a.get('content'),
                    'published_at': published_at,
                    'source_id': (a.get('source') or {}).get('id'),
                    'url_to_image': a.get('urlToImage'),
                }
            )
        except IntegrityError as e:
            print("Skipping article due to DB error:", e)

    return redirect('home')



# To do
# Add default placeholder
# Add API filter UI
# add dark mode
# add button to delete article
# verify articles before adding to db
#   are you sure you want to add 16 articles? 
#       -article1
#       -article2
#       -etc
#
#

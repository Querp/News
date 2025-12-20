from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime
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

    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])

    print(len(articles), 'articles')
    

    for a in articles:
        Article.objects.update_or_create(
            title=a['title'],  
            defaults={
                'author': a.get('author'),
                'description': a.get('description'),
                'content': a.get('content'),
                'published_at': parse_datetime(a.get('publishedAt')),
                'source_id': (a.get('source') or {}).get('id'),
                'url': a.get('url'),
                'url_to_image': a.get('urlToImage'),
            }
        )

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

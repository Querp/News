from django.urls import path
from .views.articles import (
    my_articles,
    fetch_articles_view,
    save_article,
)
from .views.sources import sources
from .views.automation import fetch_and_save_headlines

urlpatterns = [
    # path("", views.home, name="home"),
    path('', my_articles, name='my_articles'),
    path('fetch/', fetch_articles_view, name='fetch_articles'),
    path('save/', save_article, name='save_article'),
    path('sources/', sources, name='sources'),
    path("fetch_and_save_headlines/", fetch_and_save_headlines, name="fetch_and_save_headlines"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('fetch-articles/', views.fetch_articles, name='fetch_articles'),
]

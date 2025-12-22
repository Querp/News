from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('fetch/', views.fetch_articles, name='fetch_articles'),
    path('save/', views.save_article, name='save_article'),
    path('my_articles/', views.my_articles, name='my_articles'),
]

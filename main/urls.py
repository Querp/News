from django.urls import path
from . import views

urlpatterns = [
    # path("", views.home, name="home"),
    path('', views.my_articles, name='my_articles'),
    path('my_articles/', views.my_articles, name='my_articles'),
    path('fetch/', views.fetch_articles, name='fetch_articles'),
    path('save/', views.save_article, name='save_article'),
    path('sources/', views.sources, name='sources'),
    path('fetch_sources/', views.fetch_sources, name='fetch_sources'),
    path('fetch_sources_images/', views.fetch_sources_images, name='fetch_sources_images'),
]

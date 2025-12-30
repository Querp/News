from django.contrib import admin
from .models import Article
from .models import Source
from .models import ArticleLocation

admin.site.register(Article)
admin.site.register(Source)
admin.site.register(ArticleLocation)

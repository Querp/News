from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import Article
from .models import Source
from .models import ArticleLocation
from .models import GlobalFetchPreferences
from .models import FetchRun


admin.site.register(Article)
admin.site.register(Source)
admin.site.register(ArticleLocation)
admin.site.register(FetchRun)

@admin.register(GlobalFetchPreferences)
class GlobalFetchPreferencesAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": Textarea(attrs={"rows": 4, "cols": 60})},
    }
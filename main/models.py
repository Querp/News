from django.db import models
from django.utils import timezone


class Article(models.Model):
    class Origin(models.TextChoices):
        AUTO = "autoFetch", "Auto fetch"
        MANUAL = "manualFetch", "Manual fetch"
        
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField()
    source_id = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(max_length=1000, unique=True)
    url_to_image = models.URLField(max_length=1000, null=True, blank=True)
    origin = models.CharField(max_length=20, choices=Origin.choices, default=Origin.AUTO)

    def __str__(self):
        return self.title


class Source(models.Model):
    CATEGORY_CHOICES = [
        ('business', 'Business'),
        ('entertainment', 'Entertainment'),
        ('general', 'General'),
        ('health', 'Health'),
        ('science', 'Science'),
        ('sports', 'Sports'),
        ('technology', 'Technology'),
    ]
    
    api_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255, )
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    language = models.CharField(max_length=10)
    country = models.CharField(max_length=10)
    url = models.URLField()
    url_to_image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name
   
 
class ArticleLocation(models.Model):
    article = models.ForeignKey("main.Article", on_delete=models.CASCADE, related_name="locations")
    country = models.CharField(max_length=100)  
    country_code = models.CharField(max_length=2)
    state = models.CharField(max_length=100, null=True, blank=True) 
    city = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    confidence = models.FloatField(help_text="0–1 confidence score")
    is_primary = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["country_code"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        label = self.city or self.state or self.country
        return f"{label} ({self.country_code})"
    

class GlobalFetchPreferences(models.Model):
    singleton = models.BooleanField(default=True, unique=True)

    countries = models.JSONField(default=list, blank=True)
    categories = models.JSONField(default=list, blank=True)
    sources = models.JSONField(default=list, blank=True)


class FetchRun(models.Model):
    class Status(models.TextChoices):
        STARTED = "started"
        SUCCESS = "success"
        FAILED = "failed"

    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True, blank=True)

    endpoint = models.CharField(max_length=50)  # headlines / everything
    params = models.JSONField()  # countries, categories, sources, query, etc

    api_calls = models.PositiveIntegerField(default=0)

    fetched = models.PositiveIntegerField(default=0)
    saved = models.PositiveIntegerField(default=0)
    updated = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.STARTED
    )
    error = models.TextField(blank=True)

    def duration_seconds(self):
        if self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        return None

    def __str__(self):
        return f"{self.endpoint} @ {self.started_at:%Y-%m-%d %H:%M}"

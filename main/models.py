from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField()
    source_id = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(max_length=1000, unique=True)
    url_to_image = models.URLField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.title

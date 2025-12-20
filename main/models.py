from django.db import models

class Article(models.Model):
    author = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField()
    source_id = models.CharField(max_length=100, null=True, blank=True)  # just keep the ID
    url = models.URLField()
    url_to_image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

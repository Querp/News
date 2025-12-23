import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from main.models import Source


class Command(BaseCommand):
    help = "Import sources from NewsAPI (one-time)"

    def handle(self, *args, **options):
        url = "https://newsapi.org/v2/top-headlines/sources"
        params = {
            "apiKey": settings.NEWSAPI_KEY,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        sources = data.get("sources", [])

        created = 0
        skipped = 0

        for s in sources:
            # Safety: only allow known categories
            if s["category"] not in dict(Source.CATEGORY_CHOICES):
                skipped += 1
                continue

            obj, was_created = Source.objects.get_or_create(
                api_id=s["id"],
                defaults={
                    "name": s["name"],
                    "description": s.get("description", ""),
                    "category": s["category"],
                    "language": s["language"],
                    "country": s["country"],
                    "url": s["url"],
                    # url_to_image intentionally left empty
                },
            )

            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created {created} sources, skipped {skipped}."
            )
        )

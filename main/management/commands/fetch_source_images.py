from django.core.management.base import BaseCommand
from urllib.parse import urljoin
import warnings
import time

from opengraph_py3 import OpenGraph
from main.models import Source

# suppress BeautifulSoup parser warnings from opengraph_py3
warnings.filterwarnings("ignore", category=UserWarning, module="bs4")


class Command(BaseCommand):
    help = "Fetch og:image for news sources, skip CBC News explicitly"

    def handle(self, *args, **options):
        sources = Source.objects.filter(url_to_image__isnull=True)
        total = sources.count()
        updated = 0
        failed = 0

        if total == 0:
            self.stdout.write(self.style.WARNING("No sources need images."))
            return

        self.stdout.write(f"Fetching images for {total} sources...\n")

        # List of sources to skip
        skip_sources = ["CBC News"]  # you can add more names here

        for i, source in enumerate(sources, start=1):
            if source.name in skip_sources:
                self.stdout.write(f"[{i}/{total}] {source.name}: skipped explicitly")
                continue

            self.stdout.write(f"[{i}/{total}] {source.name}: fetching... ", ending="")
            self.stdout.flush()

            retries = 1
            success = False

            for attempt in range(retries + 1):
                try:
                    # set timeout per request
                    og = OpenGraph(url=source.url, timeout=10)
                    image = og.get("image")
                    if image:
                        source.url_to_image = urljoin(source.url, image)
                        source.save(update_fields=["url_to_image"])
                        updated += 1
                        self.stdout.write(self.style.SUCCESS("OK"))
                    else:
                        failed += 1
                        self.stdout.write(self.style.WARNING("No image found"))
                    success = True
                    break
                except Exception as e:
                    if attempt < retries:
                        self.stdout.write(self.style.WARNING(f"Retrying... ({e})"))
                        time.sleep(1)  # short delay before retry
                    else:
                        failed += 1
                        self.stdout.write(self.style.ERROR(f"Failed ({e})"))

        self.stdout.write("\n" + "="*50)
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Updated {updated} sources, failed {failed}."
            )
        )

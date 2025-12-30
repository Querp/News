from django.core.management.base import BaseCommand
from main.models import Article
from main.services.location_extractor import extract_locations
from main.services.geocoding import geocode_location
from main.services.score_location import score_location
from collections import Counter

class Command(BaseCommand):
    help = "Extract, normalize, rank, and save article locations"

    def handle(self, *args, **options):
        for article in Article.objects.all():
            if article.locations.exists():  # skip if already has locations
                continue
            
            text_parts = [article.title, article.description, article.content]
            text = " ".join(filter(None, text_parts))

            # Step 1: extract locations via spaCy
            raw_locations_list = extract_locations(text)
            raw_locations_list = [loc.strip() for loc in raw_locations_list if loc]
            
            if not raw_locations_list:
                continue

            # Step 2: count occurrences
            counts = Counter([loc.lower() for loc in raw_locations_list])

            # Step 3: normalize via geopy
            normalized_locations = []
            JUNK_LOCATIONS = {"Earth", "World", "Universe", "Mountains lions"}  

            for loc_name in counts:
                if loc_name.title() in JUNK_LOCATIONS:
                    continue  # skip obvious junk
                
                geo = geocode_location(loc_name)
                if geo and geo.get("country"):  # skip if country is missing
                    in_title = loc_name.lower() in article.title.lower()
                    score = score_location(geo, counts[loc_name], in_title)
                    geo["score"] = score
                    normalized_locations.append(geo)
            
            if not normalized_locations:
                continue  # skip if nothing valid after filtering
        
            # Step 4: rank locations by score
            normalized_locations.sort(key=lambda x: x["score"], reverse=True)

            # Step 5: save to DB
            from main.models import ArticleLocation
            ArticleLocation.objects.filter(article=article).delete()  # clear old locations

            for i, loc in enumerate(normalized_locations):
                ArticleLocation.objects.create(
                    article=article,
                    country=loc["country"],
                    country_code=loc["country_code"],
                    state=loc.get("state"),
                    city=loc.get("city"),
                    latitude=loc.get("lat"),
                    longitude=loc.get("lon"),
                    confidence=min(loc["score"] / 10, 1.0),
                    is_primary=(i == 0),
                )

            self.stdout.write(
                f"{article.id}: primary -> {normalized_locations[0].get('city') or normalized_locations[0].get('state') or normalized_locations[0]['country']}"
            )

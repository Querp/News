from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import logging

logging.basicConfig(level=logging.INFO)

_geolocator = Nominatim(user_agent="thenews-location-service")

_geocode = RateLimiter(
    _geolocator.geocode,
    min_delay_seconds=1,  # Respect Nominatim policy
    max_retries=3,
    error_wait_seconds=2,  # wait a bit after an error
    swallow_exceptions=False  # we want to see what fails
)

_cache: dict[str, dict | None] = {}

def geocode_location(name: str) -> dict | None:
    if not name:
        return None

    key = name.lower().strip()
    if key in _cache:
        return _cache[key]

    try:
        location = _geocode(name, timeout=15, addressdetails=True)
        if not location:
            _cache[key] = None
            logging.info(f"Location not found: {name}")
            return None

        address = location.raw.get("address", {})

        result = {
            "country": address.get("country"),
            "country_code": address.get("country_code"),
            "state": address.get("state"),
            "city": address.get("city")
            or address.get("town")
            or address.get("village"),
            "lat": location.latitude,
            "lon": location.longitude,
        }

        _cache[key] = result
        return result

    except Exception as e:
        logging.warning(f"Geocoding failed for '{name}': {e}")
        _cache[key] = None
        return None

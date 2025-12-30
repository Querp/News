from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# REQUIRED by Nominatim usage policy
_geolocator = Nominatim(user_agent="thenews-location-service")

# Respect rate limits (very important)
_geocode = RateLimiter(
    _geolocator.geocode,
    min_delay_seconds=1,
    swallow_exceptions=True,
)

# Simple in-process cache (replace later)
_cache: dict[str, dict | None] = {}


def geocode_location(name: str) -> dict | None:
    """
    Normalize a location string into structured geographic data.
    Returns None if not resolvable.
    """
    if not name:
        return None

    key = name.lower().strip()
    if key in _cache:
        return _cache[key]

    location = _geocode(name, addressdetails=True)
    if not location:
        _cache[key] = None
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

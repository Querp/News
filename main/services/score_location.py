def score_location(location: dict, count: int, in_title: bool) -> float:
    """
    location: dict from geopy
    count: number of times spaCy extracted this location
    in_title: bool, True if location appears in title
    """
    score = count
    if in_title:
        score += 2  # title hits are more important

    # city > state > country
    if location.get("city"):
        score += 2
    elif location.get("state"):
        score += 1
    # country only: 0 extra

    return score
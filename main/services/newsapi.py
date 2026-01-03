import requests
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://newsapi.org/v2/"
ENDPOINTS = {
    "everything": "everything",
    "headlines": "top-headlines",
}

def fetch_articles(
    api_key,
    query="",
    endpoint_param="everything",
    countries=None,
    categories=None,
    sources=None,
):
    """
    Fetch articles from NewsAPI, filtered by optional countries, categories, and sources.
    Supports multiple countries/categories by merging results.
    """
    api_calls = 0
    
    query = (query or "").strip()
    endpoint = ENDPOINTS.get(endpoint_param, "everything")
    countries = countries or []
    categories = categories or []
    sources = sources or []

    articles = []

    # EVERYTHING endpoint
    if endpoint == "everything":
        params = {"apiKey": api_key}
        if query:
            params["q"] = query
        if sources:
            params["sources"] = ",".join(sources)

        try:
            response = requests.get(BASE_URL + endpoint, params=params, timeout=30)
            response.raise_for_status()
            articles.extend(response.json().get("articles", []))
            api_calls += 1
        except Exception as e:
            logger.exception("Error fetching articles from everything: %s", e)

    # TOP-HEADLINES endpoint
    elif endpoint == "top-headlines":
        # NewsAPI only allows 1 country and 1 category per request
        # Loop over all combinations
        if not countries:
            countries = [None]
        if not categories:
            categories = [None]

        for country in countries:
            for category in categories:
                params = {"apiKey": api_key}
                if country:
                    params["country"] = country
                if category:
                    params["category"] = category
                if sources:
                    params["sources"] = ",".join(sources)
                if query:
                    params["q"] = query

                try:
                    response = requests.get(BASE_URL + endpoint, params=params, timeout=30)
                    response.raise_for_status()
                    articles.extend(response.json().get("articles", []))
                    api_calls += 1
                except Exception as e:
                    logger.exception(
                        "Error fetching top-headlines for country=%s category=%s: %s",
                        country,
                        category,
                        e,
                    )

    return articles, api_calls

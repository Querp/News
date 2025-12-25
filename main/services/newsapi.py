import requests
import logging
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now

logger = logging.getLogger(__name__)

BASE_URL = "https://newsapi.org/v2/"
ENDPOINTS = {
    "everything": "everything",
    "headlines": "top-headlines",
}

def fetch_articles(api_key, query="", endpoint_param="everything"):
    query = (query or "").strip()

    if endpoint_param == "everything" and not query:
        endpoint = "top-headlines"
    else:
        endpoint = ENDPOINTS.get(endpoint_param, "everything")

    params = {"apiKey": api_key}
    url = BASE_URL + endpoint

    if endpoint == "everything" and query:
        params["q"] = query
    elif endpoint == "top-headlines":
        params["country"] = "us"
        if query:
            params["q"] = query

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json().get("articles", [])

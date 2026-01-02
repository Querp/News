# main/constants/newsapi.py

NEWSAPI_COUNTRIES = {
    "ae": {"label": "United Arab Emirates",    "language": "ar"},
    "ar": {"label": "Argentina",               "language": "es"},
    "at": {"label": "Austria",                 "language": "de"},
    "au": {"label": "Australia",               "language": "en"},
    "be": {"label": "Belgium",                 "language": "nl"},
    "bg": {"label": "Bulgaria",                "language": "bg"},
    "br": {"label": "Brazil",                  "language": "pt"},
    "ca": {"label": "Canada",                  "language": "en"},
    "ch": {"label": "Switzerland",             "language": "de"},
    "cn": {"label": "China",                   "language": "zh"},
    "co": {"label": "Colombia",                "language": "es"},
    "cu": {"label": "Cuba",                    "language": "es"},
    "cz": {"label": "Czech Republic",          "language": "cs"},
    "de": {"label": "Germany",                 "language": "de"},
    "eg": {"label": "Egypt",                   "language": "ar"},
    "es": {"label": "Spain",                   "language": "es"},
    "fr": {"label": "France",                  "language": "fr"},
    "gb": {"label": "United Kingdom",          "language": "en"},
    "gr": {"label": "Greece",                  "language": "el"},
    "hk": {"label": "Hong Kong",               "language": "zh"},
    "hu": {"label": "Hungary",                 "language": "hu"},
    "id": {"label": "Indonesia",               "language": "id"},
    "ie": {"label": "Ireland",                 "language": "en"},
    "il": {"label": "Israel",                  "language": "he"},
    "in": {"label": "India",                   "language": "hi"},
    "is": {"label": "Iceland",                 "language": "is"},
    "it": {"label": "Italy",                   "language": "it"},
    "jp": {"label": "Japan",                   "language": "ja"},
    "kr": {"label": "South Korea",             "language": "ko"},
    "lt": {"label": "Lithuania",               "language": "lt"},
    "lv": {"label": "Latvia",                  "language": "lv"},
    "ma": {"label": "Morocco",                 "language": "ar"},
    "mx": {"label": "Mexico",                  "language": "es"},
    "my": {"label": "Malaysia",                "language": "ms"},
    "ng": {"label": "Nigeria",                 "language": "en"},
    "nl": {"label": "Netherlands",             "language": "nl"},
    "no": {"label": "Norway",                  "language": "no"},
    "nz": {"label": "New Zealand",             "language": "en"},
    "ph": {"label": "Philippines",             "language": "en"},
    "pk": {"label": "Pakistan",                "language": "ur"},
    "pl": {"label": "Poland",                  "language": "pl"},
    "pt": {"label": "Portugal",                "language": "pt"},
    "ro": {"label": "Romania",                 "language": "ro"},
    "rs": {"label": "Serbia",                  "language": "sr"},
    "ru": {"label": "Russia",                  "language": "ru"},
    "sa": {"label": "Saudi Arabia",            "language": "ar"},
    "se": {"label": "Sweden",                  "language": "sv"},
    "sg": {"label": "Singapore",               "language": "en"},
    "si": {"label": "Slovenia",                "language": "sl"},
    "sk": {"label": "Slovakia",                "language": "sk"},
    "th": {"label": "Thailand",                "language": "th"},
    "tr": {"label": "Turkey",                  "language": "tr"},
    "tw": {"label": "Taiwan",                  "language": "zh"},
    "ua": {"label": "Ukraine",                 "language": "uk"},
    "us": {"label": "United States",           "language": "en"},
    "ve": {"label": "Venezuela",               "language": "es"},
    "za": {"label": "South Africa",            "language": "en"},
    "zh": {"label": "China (alternate code)",  "language": "zh"},
}

CATEGORIES = [
    "business",
    "entertainment",
    "general",
    "health",
    "science",
    "sports",
    "technology",
]

# Derived helpers
SUPPORTED_COUNTRY_CODES = frozenset(NEWSAPI_COUNTRIES.keys())
DEFAULT_COUNTRY = "us"

# 👇 what templates actually need
COUNTRY_LABELS = {
    code: meta["label"]
    for code, meta in NEWSAPI_COUNTRIES.items()
}
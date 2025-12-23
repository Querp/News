from django import template
import logging

register = template.Library()
logger = logging.getLogger(__name__)

LANGUAGES = {
    "ar": "Arabic",
    "de": "German",
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "he": "Hebrew",
    "it": "Italian",
    "nl": "Dutch",
    "no": "Norwegian",
    "pt": "Portuguese",
    "ru": "Russian",
    "sv": "Swedish",
    "uk": "Ukrainian",
    "zh": "Chinese",
}

LANGUAGE_ALIASES = {
    "ud": "en",
}

def normalize_language(code):
    if not code:
        return code
    return LANGUAGE_ALIASES.get(code.lower(), code.lower())


@register.filter
def human_language(value):
    if not value:
        return ""
    
    value = normalize_language(value)
        
    if value in LANGUAGES:
        return LANGUAGES[value]
    
    logger.info(f"Country name is missing:{value}")
    return value

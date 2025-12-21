from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def human_date(value):
    if not value:
        return ""

    now = timezone.localtime()
    value = timezone.localtime(value)
    delta = (now.date() - value.date()).days

    if delta == 0:
        return "Today"
    elif delta == 1:
        return "Yesterday"
    elif delta < 7:
        return value.strftime("%A")
    else:
        return value.strftime("%B %d, %Y")

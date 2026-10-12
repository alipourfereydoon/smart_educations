"""Small template filters used by profile/dashboard templates."""
from django import template

register = template.Library()

@register.filter(name="get_item")
def get_item(dictionary, key):
    """Safely return dictionary[key], or an empty string for missing values."""
    if dictionary is None:
        return ""
    try:
        return dictionary.get(key, "")
    except AttributeError:
        try:
            return dictionary[key]
        except (KeyError, IndexError, TypeError):
            return ""

# Backwards-compatible alias: profile.html in the starter calls dict_lookup.
register.filter("dict_lookup", get_item)

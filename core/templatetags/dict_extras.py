# core/templatetags/dict_extras.py
from django import template

register = template.Library()

@register.filter
def dict_lookup(dictionary, key):
    """Template filter to lookup dictionary values"""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


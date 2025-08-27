from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """
    Template filter to lookup a value in a dictionary by key.
    Usage: {{ dict|lookup:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key, False)

@register.filter
def get_item(dictionary, key):
    """
    Alternative template filter to get an item from a dictionary.
    Usage: {{ dict|get_item:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def multiply(value, arg):
    """
    Template filter to multiply two values.
    Usage: {{ value|multiply:arg }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage(value, total):
    """
    Template filter to calculate percentage.
    Usage: {{ value|percentage:total }}
    """
    try:
        if float(total) == 0:
            return 0
        return round((float(value) / float(total)) * 100, 1)
    except (ValueError, TypeError):
        return 0

@register.filter
def dict_key(dictionary, key):
    """
    Template filter to access dictionary values by key.
    Usage: {{ dict|dict_key:key }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.simple_tag
def get_dict_value(dictionary, key):
    """
    Template tag to get dictionary value by key.
    Usage: {% get_dict_value dict key %}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
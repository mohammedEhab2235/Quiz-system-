from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key."""
    if dictionary and hasattr(dictionary, 'get'):
        return dictionary.get(key)
    return None

@register.filter
def score_percentage(score):
    """Format score as percentage for CSS width."""
    try:
        return f"{float(score):.0f}"
    except (ValueError, TypeError):
        return "0"

@register.filter
def time_format(seconds):
    """Format seconds into MM:SS format."""
    try:
        minutes = int(seconds) // 60
        seconds = int(seconds) % 60
        return f"{minutes}:{seconds:02d}"
    except (ValueError, TypeError):
        return "0:00"

@register.filter
def duration_format(start_time, end_time):
    """Calculate and format duration between two datetime objects."""
    if start_time and end_time:
        duration = end_time - start_time
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    return "N/A"
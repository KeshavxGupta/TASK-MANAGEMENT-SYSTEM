from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def adminfilter(value, arg):
    """
    Filter for admin tables to highlight active filters
    Usage: {% adminfilter field_name filter_value %}
    """
    if not value or not arg:
        return ''
    
    # Check if the current filter matches the active filter
    if value == arg:
        return mark_safe('selected')
    return '' 
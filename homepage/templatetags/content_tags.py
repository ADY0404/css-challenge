from django import template
from homepage.sanitizer import sanitize_html

register = template.Library()


@register.filter(name='safe_sanitized')
def safe_sanitized_filter(value):
    """
    Template filter to sanitize HTML and render it safely.
    Example: {{ section.body|safe_sanitized }}
    """
    if not value:
        return ""
    return sanitize_html(value)


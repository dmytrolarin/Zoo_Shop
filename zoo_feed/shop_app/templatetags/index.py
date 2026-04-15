from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    """
    Return an item from an indexable object by its index.
    """
    return indexable[i]

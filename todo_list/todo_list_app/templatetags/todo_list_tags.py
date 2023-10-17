from django import template



register = template.Library()

@register.filter(name='is_null_or_false')
def is_null_or_false(value):
    """Returns 'Not specified' if value is None or False, else returns value"""
    if value:
        return value
    else:
        return 'Not specified'

@register.filter(name='get_length_or_empty')
def get_length_or_empty(queryset):
    """Returns False if queryset is empty, else returns length of queryset"""
    if queryset != []:
        return len(queryset)
    else:
        return False

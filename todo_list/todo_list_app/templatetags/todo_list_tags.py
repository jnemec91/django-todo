from django import template



register = template.Library()

@register.filter(name='is_null_or_false')
def is_null_or_false(value):
    if value:
        return value
    else:
        return 'Not specified'

@register.filter(name='is_empty')
def is_empty(queryset):
    if queryset != []:
        return len(queryset)
    else:
        return False

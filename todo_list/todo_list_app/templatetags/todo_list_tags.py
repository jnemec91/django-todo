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

@register.filter(name='get_item')
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        """Returns value of dictionary[key]"""
        return dictionary.get(key)
    
    elif isinstance(dictionary, list):
        """Returns value of list[(tuple)[key]]"""
        try:
            for i in dictionary:
                if i[0] == key:
                    
                    return i[1]
        except (IndexError, KeyError):
            return False

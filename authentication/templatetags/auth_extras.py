from django import template

register = template.Library()

@register.filter
def get_field(form, index):
    """Get a field from a form by index"""
    try:
        return list(form)[index]
    except (IndexError, TypeError):
        return None

@register.filter
def attr(obj, attribute):
    """Get an attribute from an object"""
    try:
        return getattr(obj, attribute)
    except AttributeError:
        return None

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary"""
    try:
        return dictionary[key]
    except (KeyError, TypeError):
        return None

@register.filter
def addstr(arg1, arg2):
    """Concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)
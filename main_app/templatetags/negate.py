from django import template
register = template.Library()

@register.filter(name="negate")
def star(value):
    return -value
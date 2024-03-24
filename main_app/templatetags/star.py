from django import template
register = template.Library()

@register.filter(name="star")
def star(value):
    starstring="s"*value
    return starstring
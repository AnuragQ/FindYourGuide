from django import template

register = template.Library()

@register.filter
def stars(value):
    full_stars = int(value)
    half_star = round(value - full_stars)
    empty_stars = 5 - full_stars - half_star

    return {
        'full_stars': range(full_stars),
        'half_star': half_star,
        'empty_stars': range(empty_stars),
    }
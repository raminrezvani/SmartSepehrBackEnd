from django import template

register = template.Library()


def price_filter(price):
    return '{:,}'.format(int(float(price)))


register.filter('price_filter', price_filter)

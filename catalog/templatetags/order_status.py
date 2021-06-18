from django import template

register = template.Library()


@register.filter
def order_status(values):
    return eval('v')

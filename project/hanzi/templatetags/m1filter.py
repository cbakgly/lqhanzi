from django import template

register = template.Library()


@register.filter(name='key')
@register.filter(name='list')
def key(d, key_name):
    # value = 0
    # try:
    value = d[key_name]
    # except KeyError:
    # value = 0
    return value


def list(d, index):
    # value = 0
    # try:
    value = d[index]
    # except KeyError:
    # value = 0
    return value

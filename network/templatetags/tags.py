from django import template

register = template.Library()

@register.filter
def ifinlist(usr, lst):
    return usr in lst
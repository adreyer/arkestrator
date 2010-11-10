from urlparse import urlparse
from django import template

register = template.Library()

@register.filter
def domain(url):
    return urlparse(url)[1]

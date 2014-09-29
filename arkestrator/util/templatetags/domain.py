from urlparse import urlparse
from django import template

register = template.Library()

@register.filter
def domain(url):
    """ extract the domainname from a url """
    return urlparse(url)[1]

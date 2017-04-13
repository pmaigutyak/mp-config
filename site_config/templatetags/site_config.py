
from django import template

from .. import config


register = template.Library()


@register.assignment_tag
def get_site_config():
    return config

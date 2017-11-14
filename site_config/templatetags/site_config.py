
from django import template


from .. import config


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_site_config(context):
    return config

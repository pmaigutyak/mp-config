
from django import template


from .. import SiteConfig


register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_config(context):
    return SiteConfig()

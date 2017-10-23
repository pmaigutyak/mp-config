
from django import template


from .. import get_config_for_site


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_site_config(context):
    return get_config_for_site(getattr(context, 'request'))

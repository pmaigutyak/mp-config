
from django.apps import apps, AppConfig
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.conf import settings


default_app_config = 'site_config.SiteConfigApp'

__version__ = '2.0'

__all__ = ['default_app_config', 'SiteConfig', 'get_config_for_site']


class SiteConfigApp(AppConfig):
    name = 'site_config'
    verbose_name = _("Settings")


class SiteConfig(object):

    def __init__(self, site_id):
        self._site_id = site_id

    def __getattr__(self, name):
        if name.startswith('_'):
            return super(SiteConfig, self).__getattribute__(name)

        return self._get_field(name).value

    def __setattr__(self, key, value):
        if key.startswith('_'):
            super(SiteConfig, self).__setattr__(key, value)
        else:
            self._get_field(key).value = value

    @cached_property
    def _fields(self):
        field_model = apps.get_model('site_config', 'ConfigField')
        fields = field_model.objects.filter(site_id=self._site_id)
        return {f.name: f for f in fields}

    def _get_field(self, name):
        try:
            return self._fields[name]
        except KeyError:
            raise AttributeError("Site config has no field named '%s'" % name)


def get_config_for_site(request=None):

    if request:
        host = request.META.get('HTTP_HOST')
        site_model = apps.get_model('sites', 'Site')

        try:
            site = site_model.objects.get(domain=host)
            return SiteConfig(site.id)
        except site_model.DoesNotExist:
            pass

    return SiteConfig(settings.SITE_ID)

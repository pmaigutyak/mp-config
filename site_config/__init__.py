
from django.apps import apps, AppConfig
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.conf import settings


default_app_config = 'site_config.SiteConfigApp'

__version__ = '3.3'

__all__ = ['default_app_config', 'SiteConfig']


class SiteConfigApp(AppConfig):
    name = 'site_config'
    verbose_name = _("Settings")


class SiteConfig(object):

    def __init__(self):
        self._updated_fields = []

    def __getattr__(self, name):
        if name.startswith('_'):
            return super(SiteConfig, self).__getattribute__(name)

        return self._get_field(name).value

    def __setattr__(self, key, value):
        if key.startswith('_'):
            super(SiteConfig, self).__setattr__(key, value)
        else:
            self._get_field(key).value = value
            self._updated_fields.append(key)

    @cached_property
    def _fields(self):
        field_model = apps.get_model('site_config', 'ConfigField')
        fields = field_model.objects.filter(site_id=settings.SITE_ID)
        return {f.name: f for f in fields}

    def _get_field(self, name):
        try:
            return self._fields[name]
        except KeyError:
            raise AttributeError("Site config has no field named '%s'" % name)

    def save(self):
        for f_name, field in self._fields.items():
            if f_name in self._updated_fields:
                field.save()

        self._updated_fields = []

    def reload(self):
        try:
            del self.__dict__['_fields']
        except KeyError:
            pass

config = SiteConfig()

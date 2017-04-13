
from django.apps import apps


class SiteConfig(object):

    def __getattr__(self, name):
        if name.startswith('_'):
            return super(SiteConfig, self).__getattribute__(name)

        return self._get_field(name).value

    def __setattr__(self, key, value):
        if key.startswith('_'):
            super(SiteConfig, self).__setattr__(key, value)
        else:
            self._get_field(key).value = value

    def _get_fields(self):
        if not hasattr(self, '_fields'):
            field_model = apps.get_model('site_config', 'ConfigField')
            self._fields = {f.name: f for f in field_model.objects.all()}

        return self._fields

    def _get_field(self, name):
        try:
            return self._get_fields()[name]
        except KeyError:
            raise AttributeError("Site config has no field named '%s'" % name)


config = SiteConfig()


__version__ = '1.0'

__all__ = ['config']

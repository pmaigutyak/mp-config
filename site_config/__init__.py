
from django.apps import apps
from django.utils.functional import SimpleLazyObject


def setup_settings(settings, is_prod, **kwargs):

    for template in settings['TEMPLATES']:
        template['OPTIONS']['context_processors'].append(
            'site_config.context_processors.config')


class SiteConfig:

    def __getattr__(self, name):

        if name.startswith('_'):
            return super(SiteConfig, self).__getattribute__(name)

        if not hasattr(self, '_cached_fields'):
            self._cached_fields = self.get_fields()

        if name in self._cached_fields:
            return self._cached_fields[name].value

        return None

    def get_fields(self):
        from site_config.models import ConfigField
        return {f.name: f for f in ConfigField.objects.all()}

    def reload(self):
        if hasattr(self, '_cached_fields'):
            del self._cached_fields


config = SimpleLazyObject(lambda: SiteConfig())

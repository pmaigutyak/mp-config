
from django.apps import apps, AppConfig
from django.utils.translation import gettext_lazy as _


def setup_settings(settings, is_prod, **kwargs):

    if 'djckeditor' not in settings['INSTALLED_APPS']:
        settings['INSTALLED_APPS'] += ['djckeditor']

    for template in settings['TEMPLATES']:
        template['OPTIONS']['context_processors'].append(
            'site_config.context_processors.config')


default_app_config = 'site_config.SiteConfigApp'


class SiteConfigApp(AppConfig):
    name = 'site_config'
    verbose_name = _("Settings")

    def ready(self):
        if not apps.is_installed("ckeditor"):
            raise Exception("Please add `ckeditor` to `INSTALLED_APPS`.")

class SiteConfig(object):

    def __getattr__(self, name):

        if name.startswith('_'):
            return super(SiteConfig, self).__getattribute__(name)

        if not hasattr(self, '_cached_fields'):
            self._cached_fields = self.get_fields()

        if name in self._cached_fields:
            return self._cached_fields[name].value

        return None

    def get_fields(self):
        fields = apps.get_model('site_config', 'ConfigField').objects.all()
        return {f.name: f for f in fields}

    def reload(self):
        if hasattr(self, '_cached_fields'):
            del self._cached_fields


config = SiteConfig()

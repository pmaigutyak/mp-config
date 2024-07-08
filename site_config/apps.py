from django.apps import AppConfig, apps
from django.utils.translation import gettext_lazy as _


class SiteConfigApp(AppConfig):
    name = 'site_config'
    verbose_name = _("Settings")

    def ready(self):
        if not apps.is_installed("django_prose_editor"):
            raise Exception(
                "Please add `django_prose_editor` to `INSTALLED_APPS`.")


from django.apps import apps
from django.contrib import admin

from site_config.models import ConfigField
from site_config import config


def _get_parent_admin_classes():

    if apps.is_installed('modeltranslation'):
        from modeltranslation.admin import TranslationAdmin
        classes = [TranslationAdmin]
    else:
        classes = [admin.ModelAdmin]

    if apps.is_installed('import_export'):

        from import_export.resources import ModelResource
        from import_export.admin import ImportExportMixin, ExportActionMixin

        class ConfigFieldResource(ModelResource):
            class Meta:
                model = ConfigField
                exclude = ('id', )

        class ImportExportAdmin(
                ImportExportMixin,
                ExportActionMixin):

            actions_on_bottom = False
            resource_class = ConfigFieldResource

        classes.append(ImportExportAdmin)

    return classes


@admin.register(ConfigField)
class ConfigFieldAdmin(*_get_parent_admin_classes()):

    CONFIG_FIELDS = ['label', 'name', 'type', 'splitter']

    list_display = [
        'label', 'name', 'type', 'splitter', 'short_value']

    list_per_page = 200

    def save_model(self, *args, **kwargs):
        super(ConfigFieldAdmin, self).save_model(*args, **kwargs)
        config.reload()

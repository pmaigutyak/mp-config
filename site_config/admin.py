
from importlib import import_module

from django.apps import apps
from django.contrib import admin

from site_config.models import ConfigField, ConfigGroup, HTMLField
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
                exclude = ('id', 'group', )

        class ImportExportAdmin(
                ImportExportMixin,
                ExportActionMixin):

            actions_on_bottom = False
            resource_class = ConfigFieldResource

        classes.append(ImportExportAdmin)

    return classes


class ConfigFieldAdmin(*_get_parent_admin_classes()):

    CONFIG_FIELDS = ['group', 'label', 'name', 'type', 'splitter']

    list_display = [
        'label', 'name', 'type', 'splitter', 'short_value', 'group']

    list_filter = ['group']

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if apps.is_installed('ckeditor_uploader'):
            from ckeditor_uploader.widgets import CKEditorUploadingWidget
            self.formfield_overrides = {
                HTMLField: {'widget': CKEditorUploadingWidget}
            }

        elif apps.is_installed('ckeditor'):
            from ckeditor.widgets import CKEditorWidget
            self.formfield_overrides = {
                HTMLField: {'widget': CKEditorWidget}
            }

    def save_model(self, *args, **kwargs):
        super(ConfigFieldAdmin, self).save_model(*args, **kwargs)
        config.reload()


admin.site.register(ConfigField, ConfigFieldAdmin)
admin.site.register(ConfigGroup)

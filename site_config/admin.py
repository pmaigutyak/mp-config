
from django.apps import apps
from django.db import models
from django.contrib import admin

from modeltranslation.utils import get_translation_fields
from modeltranslation.admin import TranslationAdmin

from site_config.models import ConfigField, ConfigGroup


class ConfigFieldAdmin(TranslationAdmin):

    list_display = [
        'label', 'name', 'type', 'splitter', 'short_value', 'group']

    list_filter = ['group']

    def _get_config_fields(self, obj=None):

        if obj is None:
            return ['group', 'label', 'name', 'type', 'splitter']

        f_name = obj.value_field_name

        if f_name in self.trans_opts.fields:
            return get_translation_fields(f_name)

        return [f_name]

    def get_form(self, request, obj=None, fields=None, **kwargs):

        fields = self._get_config_fields(obj)

        if apps.is_installed('ckeditor_uploader'):
            from ckeditor_uploader.widgets import CKEditorUploadingWidget
            self.formfield_overrides = {
                models.TextField: {'widget': CKEditorUploadingWidget}
            }

        elif apps.is_installed('ckeditor'):
            from ckeditor.widgets import CKEditorWidget
            self.formfield_overrides = {
                models.TextField: {'widget': CKEditorWidget}
            }

        return super(ConfigFieldAdmin, self).get_form(
            request, obj=obj, fields=fields, **kwargs)


admin.site.register(ConfigField, ConfigFieldAdmin)
admin.site.register(ConfigGroup)

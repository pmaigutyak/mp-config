
from importlib import import_module

from django.apps import apps
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from site_config.models import ConfigField, ConfigGroup
from site_config import config


def _get_config_field_admin_base_class():

    if apps.is_installed('modeltranslation'):
        return import_module('modeltranslation.admin').TranslationAdmin

    return admin.ModelAdmin


class ConfigFieldAdmin(_get_config_field_admin_base_class()):

    CONFIG_FIELDS = ['site', 'group', 'label', 'name', 'type', 'splitter']

    list_display = [
        'label', 'name', 'site', 'type', 'splitter', 'short_value', 'group']

    list_filter = ['site', 'group']

    def _get_value_fields(self, obj=None):

        f_name = obj.value_field_name

        if apps.is_installed('modeltranslation'):

            from modeltranslation.utils import get_translation_fields

            if f_name in self.trans_opts.fields:
                return get_translation_fields(f_name)

        return [f_name]

    def get_form(self, request, obj=None, fields=None, **kwargs):

        if obj is None:
            fields = self.CONFIG_FIELDS
        else:
            self.fieldsets = (
                (
                    _('Value'),
                    {
                        'fields': self._get_value_fields(obj)
                    }
                ),
                (
                    _('Settings'),
                    {
                        'fields': self.CONFIG_FIELDS,
                        'classes': ['collapse'],
                    }
                ),
            )

        if obj is not None and obj.is_html:
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

    def save_model(self, *args, **kwargs):
        super(ConfigFieldAdmin, self).save_model(*args, **kwargs)
        config.reload()


admin.site.register(ConfigField, ConfigFieldAdmin)
admin.site.register(ConfigGroup)

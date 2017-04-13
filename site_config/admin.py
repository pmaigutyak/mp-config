
from django.contrib import admin

from modeltranslation.utils import get_translation_fields
from modeltranslation.admin import TranslationAdmin

from site_config.models import ConfigField


class ConfigFieldAdmin(TranslationAdmin):

    list_display = ['label', 'name', 'type', 'splitter']

    def get_form(self, request, obj=None, fields=None, **kwargs):

        if obj is not None:
            fields = get_translation_fields(obj.value_field_name)
        else:
            fields = ['label', 'name', 'type', 'splitter']

        return super(ConfigFieldAdmin, self).get_form(
            request, obj=obj, fields=fields, **kwargs)


admin.site.register(ConfigField, ConfigFieldAdmin)

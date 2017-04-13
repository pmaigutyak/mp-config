
from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from site_config.models import ConfigField


class ConfigFieldAdmin(TranslationAdmin):

    list_display = ['label', 'name', 'type', 'splitter']

    fields = ['label', 'name', 'type', 'splitter']

    def get_fields(self, request, obj=None):

        if obj is not None:
            return [obj.value_field_name]

        return self.fields


admin.site.register(ConfigField, ConfigFieldAdmin)

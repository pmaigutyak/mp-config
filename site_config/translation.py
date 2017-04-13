
from modeltranslation.translator import translator, TranslationOptions

from site_config.models import ConfigField


class ConfigFieldTranslationOptions(TranslationOptions):
    fields = ('value_input', 'value_text', )


translator.register(ConfigField, ConfigFieldTranslationOptions)

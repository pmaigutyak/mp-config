
from modeltranslation.translator import translator

from site_config.models import ConfigField


translator.register(
    ConfigField, fields=['value_input', 'value_text', 'value_html'])

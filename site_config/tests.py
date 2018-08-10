
from django.test import TestCase
from django.core.management import call_command

from site_config.models import ConfigField
from site_config import SiteConfig

FIELD_TYPE_INPUT = 'input'
FIELD_TYPE_TEXT = 'text'
FIELD_TYPE_HTML = 'html'
FIELD_TYPE_JSON = 'json'

COMMA_SPLITTER = ','


class SiteConfigTestCase(TestCase):

    def setUp(self):
        call_command('sync_translation_fields', interactive=False)

    def test_config_returns_input_value(self):

        ConfigField.objects.create(
            label='Test',
            name='test',
            type=FIELD_TYPE_INPUT,
            value_input='test value')

        config = SiteConfig()

        self.assertEqual(config.test, 'test value')

    def test_config_returns_correct_value_splitted_by_comma(self):

        ConfigField.objects.create(
            label='Test',
            name='test',
            splitter=COMMA_SPLITTER,
            type=FIELD_TYPE_INPUT,
            value_input='test,value')

        config = SiteConfig()

        val = config.test

        self.assertEqual(len(val), 2)
        self.assertEqual(val[0], 'test')
        self.assertEqual(val[1], 'value')

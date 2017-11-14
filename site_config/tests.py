
from django.test import TestCase
from django.core.management import call_command

from site_config.models import ConfigField
from site_config import SiteConfig


SITE_1_ID = 1
SITE_2_ID = 2

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
            site_id=SITE_1_ID,
            label='Test',
            name='test',
            type=FIELD_TYPE_INPUT,
            value_input='test value')

        config = SiteConfig()

        self.assertEqual(config.test, 'test value')

    def test_config_raises_error_when_field_is_from_other_site(self):

        ConfigField.objects.create(
            site_id=SITE_1_ID,
            label='Test',
            name='test',
            type=FIELD_TYPE_INPUT,
            value_input='test value')

        config = SiteConfig()

        self.assertRaises(AttributeError, lambda: config.test)

    def test_config_returns_correct_value_splitted_by_comma(self):

        ConfigField.objects.create(
            site_id=SITE_1_ID,
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

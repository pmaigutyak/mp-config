
import json

from bs4 import BeautifulSoup

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site
from django.utils.encoding import python_2_unicode_compatible


FIELD_TYPE_INPUT = 'input'
FIELD_TYPE_TEXT = 'text'
FIELD_TYPE_HTML = 'html'
FIELD_TYPE_JSON = 'json'

FIELD_TYPES = (
    (FIELD_TYPE_INPUT, _("Input")),
    (FIELD_TYPE_TEXT, _("Text")),
    (FIELD_TYPE_HTML, _("HTML")),
    ('int', _("Integer")),
    ('float', _("Float")),
    ('bool', _("True / False")),
    ('url', _("Url")),
    ('email', _("Email")),
    ('file', _("File")),
    ('image', _("Image")),
    (FIELD_TYPE_JSON, _('JSON')),
)


NEWLINE_SPLITTER = 'newline'

SPLIT_CHOICES = (
    (NEWLINE_SPLITTER, _('New line')),
    (',', _('Comma')),
    ('.', _('Dot')),
    (';', _('Semicolon')),
    (' ', _('Tab')),
)


@python_2_unicode_compatible
class ConfigGroup(models.Model):

    name = models.CharField(_('Name'), max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Config group')
        verbose_name_plural = _('Config groups')


@python_2_unicode_compatible
class ConfigField(models.Model):

    SPLIT_TYPES = [FIELD_TYPE_TEXT, FIELD_TYPE_INPUT]

    site = models.ForeignKey(
        Site, verbose_name=_('Site'), default=settings.SITE_ID,
        on_delete=models.CASCADE)

    group = models.ForeignKey(
        ConfigGroup, null=True, blank=True, verbose_name=_('Group'),
        on_delete=models.CASCADE)

    label = models.CharField(_('Label'), max_length=255)

    name = models.CharField(_('Name'), max_length=255)

    type = models.CharField(_('Type'), max_length=50, choices=FIELD_TYPES)

    splitter = models.CharField(
        _('Splitter'), max_length=10, blank=True, null=True,
        choices=SPLIT_CHOICES,
        help_text=_('Available only for types: %s') % ', '.join(SPLIT_TYPES))

    value_input = models.CharField(
        _('Input'), max_length=255, blank=True, null=True)

    value_text = models.TextField(
        _('Text'), max_length=10000, blank=True, null=True)

    value_int = models.IntegerField(_('Integer'), blank=True, null=True)

    value_float = models.IntegerField(_('Float'), blank=True, null=True)

    value_bool = models.NullBooleanField(_('Boolean'), blank=True)

    value_url = models.URLField(_('Url'), blank=True, null=True)

    value_email = models.EmailField(_('Email'), blank=True, null=True)

    value_file = models.FileField(
        _('File'), blank=True, null=True, upload_to='site_config')

    value_image = models.ImageField(
        _('Image'), blank=True, null=True, upload_to='site_config')

    value_json = models.TextField(
        _('Text'), max_length=10000, blank=True, null=True)

    def __str__(self):
        return self.label

    @property
    def value_field_name(self):
        if self.type == FIELD_TYPE_HTML:
            return 'value_%s' % FIELD_TYPE_TEXT
        return 'value_%s' % self.type

    def get_splitter(self):
        splitter = self.splitter

        if splitter == NEWLINE_SPLITTER:
            splitter = '\n'

        return splitter

    @property
    def short_value(self):

        value = self.value

        if isinstance(value, list):
            value = ', '.join(value)

        if self.is_html:
            soup = BeautifulSoup(value, 'html.parser')
            return soup.get_text()[:255]

        if self.type == FIELD_TYPE_TEXT:
            return value[:255]

        return value

    short_value.fget.short_description = _('Short value')

    def _get_value(self):

        value = getattr(self, self.value_field_name)

        if not value:
            return ''

        if self.is_html:
            return mark_safe(value)

        if self.type == FIELD_TYPE_JSON:
            return json.loads(value)

        splitter = self.get_splitter()

        if self.type in self.SPLIT_TYPES and splitter is not None:
            return value.split(splitter)

        return value

    def _set_value(self, value):
        setattr(self, self.value_field_name, value)

    @property
    def is_html(self):
        return self.type == FIELD_TYPE_HTML

    value = property(_get_value, _set_value)

    class Meta:
        unique_together = ['site', 'name']
        ordering = ['label']
        verbose_name = verbose_name_plural = _('settings')


from django.db import models
from django.utils.translation import ugettext_lazy as _


FIELD_TYPE_INPUT = 'input'
FIELD_TYPE_TEXT = 'text'

FIELD_TYPES = (
    (FIELD_TYPE_INPUT, _("Input")),
    (FIELD_TYPE_TEXT, _("Text")),
    ('int', _("Integer")),
    ('float', _("Float")),
    ('bool', _("True / False")),
    ('url', _("Url")),
    ('email', _("Email")),
    ('file', _("File")),
    ('image', _("Image")),
    ('json', _('JSON')),
)


NEWLINE_SPLITTER = 'newline'

SPLIT_CHOICES = (
    (NEWLINE_SPLITTER, _('New line')),
    (',', _('Comma')),
    ('.', _('Dot')),
    (';', _('Semicolon')),
    (' ', _('Tab')),
)


class ConfigGroup(models.Model):

    name = models.CharField(_('Name'), max_length=255, unique=True)


class ConfigField(models.Model):

    SPLIT_TYPES = [FIELD_TYPE_TEXT, FIELD_TYPE_INPUT]

    group = models.ForeignKey(ConfigGroup, null=True)

    label = models.CharField(_('Label'), max_length=255)

    name = models.CharField(_('Name'), max_length=255)

    type = models.CharField(_('Type'), max_length=50, choices=FIELD_TYPES)

    splitter = models.CharField(
        _('Splitter'), max_length=10, blank=True, null=True,
        choices=SPLIT_CHOICES,
        help_text=_('Available only for types: %s') % ', '.join(SPLIT_TYPES))

    value_input = models.CharField(
        _('Text'), max_length=255, blank=True, null=True)

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

    def __unicode__(self):
        return self.label

    @property
    def value_field_name(self):
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

        if self.type == FIELD_TYPE_TEXT:
            return value[:255]

        return value

    short_value.fget.short_description = _('Short value')

    def _get_value(self):

        value = getattr(self, self.value_field_name)

        if not value:
            return ''

        splitter = self.get_splitter()

        if self.type in self.SPLIT_TYPES and splitter is not None:
            return value.split(splitter)

        return value

    def _set_value(self, value):
        setattr(self, self.value_field_name, value)

    value = property(_get_value, _set_value)

    class Meta:
        ordering = ['type']
        verbose_name = verbose_name_plural = _('settings')

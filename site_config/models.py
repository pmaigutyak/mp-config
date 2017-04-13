
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


FIELD_TYPES = (
    ('input', _("Input")),
    ('text', _("Text")),
    ('int', _("Integer")),
    ('float', _("Float")),
    ('bool', _("True / False")),
    ('url', _("Url")),
    ('email', _("Email")),
    ('file', _("File")),
    ('image', _("Image")),
)


NEWLINE_SPLITTER = 'newline'

SPLIT_CHOICES = (
    (NEWLINE_SPLITTER, _('New line')),
    (',', _('Comma')),
    ('.', _('Dot')),
    (';', _('Semicolon')),
    (' ', _('Tab')),
)


class ConfigField(models.Model):

    label = models.CharField(_('Label'), max_length=255)

    name = models.CharField(_('Name'), max_length=255)

    type = models.CharField(_('Type'), max_length=50, choices=FIELD_TYPES)

    splitter = models.CharField(
        _('Splitter'), max_length=10, blank=True, null=True,
        choices=SPLIT_CHOICES)

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

    def _get_value(self):

        value = getattr(self, self.value_field_name)

        if not value:
            return ''

        splitter = self.get_splitter()

        if self.type in ['input', 'text'] and splitter is not None:
            return value.split(mark_safe(splitter))

        return value

    def _set_value(self, value):
        setattr(self, self.value_field_name, value)

    value = property(_get_value, _set_value)

    class Meta:
        ordering = ['type']
        verbose_name = verbose_name_plural = _('settings')

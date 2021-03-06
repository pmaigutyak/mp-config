# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-07-14 10:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_config', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configfield',
            name='value_json',
            field=models.TextField(blank=True, max_length=10000, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='configfield',
            name='splitter',
            field=models.CharField(blank=True, choices=[(b'newline', 'New line'), (b',', 'Comma'), (b'.', 'Dot'), (b';', 'Semicolon'), (b' ', 'Tab')], help_text='\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e \u0442\u0456\u043b\u044c\u043a\u0438 \u0434\u043b\u044f \u0442\u0438\u043f\u0456\u0432: text, input', max_length=10, null=True, verbose_name='Splitter'),
        ),
        migrations.AlterField(
            model_name='configfield',
            name='type',
            field=models.CharField(choices=[(b'input', 'Input'), (b'text', 'Text'), (b'int', 'Integer'), (b'float', 'Float'), (b'bool', 'True / False'), (b'url', 'Url'), (b'email', 'Email'), (b'file', 'File'), (b'image', 'Image'), (b'json', 'JSON')], max_length=50, verbose_name='Type'),
        ),
    ]

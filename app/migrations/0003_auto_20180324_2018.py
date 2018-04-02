# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-24 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180324_1932'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parsedrecipe',
            old_name='environment',
            new_name='environment_state',
        ),
        migrations.AddField(
            model_name='parsedrecipe',
            name='cycle',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parsedrecipe',
            name='environment_name',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
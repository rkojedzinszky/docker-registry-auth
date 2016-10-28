# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 06:53
from __future__ import unicode_literals

from django.db import migrations
from django.db.migrations.operations import RenameField


class Migration(migrations.Migration):

    dependencies = [
        ('dra', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='repository',
            options={'verbose_name_plural': 'Repositories'},
        ),
        migrations.RenameField(
            model_name='RepositoryPermissions',
            old_name='group',
            new_name='sgroup'),
    ]

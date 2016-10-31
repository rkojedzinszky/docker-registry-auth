# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 09:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('public', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Repositories',
            },
        ),
        migrations.CreateModel(
            name='RepositoryPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('write', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dra.Group')),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dra.Repository')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='groups',
            field=models.ManyToManyField(to='dra.Group'),
        ),
        migrations.AlterUniqueTogether(
            name='repositorypermissions',
            unique_together=set([('repository', 'group')]),
        ),
    ]
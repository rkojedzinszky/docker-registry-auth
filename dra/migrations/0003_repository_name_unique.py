# Generated by Django 2.2.7 on 2020-09-25 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dra', '0002_auto_20161109_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
# Generated by Django 3.0.7 on 2020-06-09 14:45

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0002_auto_20200609_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.SlugField(), blank=True, null=True, size=None),
        ),
    ]

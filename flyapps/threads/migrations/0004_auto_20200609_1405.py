# Generated by Django 3.0.7 on 2020-06-09 13:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0003_auto_20200609_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.SlugField(null=True), blank=True, null=True, size=None),
        ),
    ]

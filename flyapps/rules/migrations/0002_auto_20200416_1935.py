# Generated by Django 3.0.5 on 2020-04-16 18:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='rules', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rule',
            name='penalties',
            field=models.ManyToManyField(to='rules.Penalty'),
        ),
    ]

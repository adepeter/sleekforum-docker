# Generated by Django 3.0.7 on 2020-06-16 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chats', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='replies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='messageview',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_views', to='chats.Message'),
        ),
        migrations.AddField(
            model_name='messageview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_views', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='messages_received', to=settings.AUTH_USER_MODEL, verbose_name='Receiver'),
        ),
        migrations.AddField(
            model_name='message',
            name='starter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='messages_started', to=settings.AUTH_USER_MODEL, verbose_name='Sender'),
        ),
    ]

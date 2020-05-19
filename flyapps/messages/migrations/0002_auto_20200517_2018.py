# Generated by Django 3.0.6 on 2020-05-17 19:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='messages_received', to=settings.AUTH_USER_MODEL, verbose_name='Receiver'),
        ),
        migrations.AlterField(
            model_name='message',
            name='starter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='messages_started', to=settings.AUTH_USER_MODEL, verbose_name='Sender'),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(unique_for_date='created', verbose_name='text'),
        ),
        migrations.CreateModel(
            name='MessageFlag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag', models.CharField(choices=[('FN', 'New'), ('FA', 'Active'), ('FE', 'Engaged')], default='FN', max_length=2, verbose_name='flag')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_statuses', to='contenttypes.ContentType')),
            ],
        ),
    ]

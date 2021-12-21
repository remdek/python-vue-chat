# Generated by Django 4.0 on 2021-12-21 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('chat_ws', '0003_remove_msg_opponent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='msg',
            name='owner',
        ),
        migrations.AddField(
            model_name='msg',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user', to='users.user', verbose_name='Владелец'),
            preserve_default=False,
        ),
    ]
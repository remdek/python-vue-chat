# Generated by Django 4.0 on 2021-12-21 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat_ws', '0002_remove_msg_student_msg_owner_alter_msg_lesson_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='msg',
            name='opponent',
        ),
    ]
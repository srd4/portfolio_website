# Generated by Django 4.1.2 on 2022-12-22 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skill_set', '0006_lesson_skills'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='lessons',
        ),
    ]

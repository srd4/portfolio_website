# Generated by Django 4.1.2 on 2022-12-22 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skill_set', '0004_lesson_active_skill_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='active',
        ),
    ]

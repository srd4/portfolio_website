# Generated by Django 4.1.2 on 2022-12-22 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skill_set', '0003_lesson_parent_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='skill',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]

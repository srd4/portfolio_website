# Generated by Django 4.1.2 on 2023-01-20 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skill_set', '0007_remove_skill_lessons'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='link',
            new_name='code_link',
        ),
    ]

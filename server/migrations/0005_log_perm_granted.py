# Generated by Django 5.1.4 on 2025-01-28 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_alter_door_descriptor_alter_door_perm_level_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='perm_granted',
            field=models.BooleanField(default=True),
        ),
    ]

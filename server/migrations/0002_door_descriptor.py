# Generated by Django 5.1.4 on 2025-01-23 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='door',
            name='descriptor',
            field=models.CharField(default='Door description', max_length=200),
        ),
    ]

# Generated by Django 5.1.6 on 2025-03-18 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_calendar', '0013_customcalendar_format'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customcalendar',
            name='format',
            field=models.CharField(default='Table', max_length=100),
        ),
    ]

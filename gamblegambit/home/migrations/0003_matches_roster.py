# Generated by Django 3.1.2 on 2021-01-15 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210113_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='matches',
            name='roster',
            field=models.JSONField(blank=True, null=True),
        ),
    ]

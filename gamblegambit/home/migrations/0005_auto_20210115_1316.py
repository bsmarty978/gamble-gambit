# Generated by Django 3.1.2 on 2021-01-15 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20210115_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='matches',
            name='photos',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='result',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
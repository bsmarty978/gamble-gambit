# Generated by Django 3.1.2 on 2021-01-25 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('create_team', '0002_myteam'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myteam',
            name='user_team',
        ),
    ]

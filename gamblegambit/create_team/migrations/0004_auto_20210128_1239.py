# Generated by Django 3.1.2 on 2021-01-28 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_team', '0003_remove_myteam_user_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='matches',
            name='team_a_photos',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='matches',
            name='team_b_photos',
            field=models.JSONField(blank=True, null=True),
        ),
    ]

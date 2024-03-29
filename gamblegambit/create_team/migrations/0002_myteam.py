# Generated by Django 3.1.2 on 2021-01-25 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('create_team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10)),
                ('user_team', models.JSONField()),
                ('user_captain', models.CharField(max_length=10)),
                ('user_roster', models.JSONField()),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='create_team.matches')),
            ],
        ),
    ]

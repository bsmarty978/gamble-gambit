# Generated by Django 3.1.2 on 2021-01-13 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UpcomingMatchesList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('team_a', models.CharField(max_length=10)),
                ('team_b', models.CharField(max_length=10)),
                ('team_a_flag', models.URLField(blank=True)),
                ('team_b_flag', models.URLField(blank=True)),
                ('game', models.CharField(max_length=20)),
                ('competation', models.CharField(blank=True, max_length=20)),
                ('time', models.CharField(max_length=20)),
                ('time_obj', models.DateTimeField()),
                ('result', models.JSONField()),
                ('isUpcoming', models.BooleanField()),
                ('isOngoiing', models.BooleanField()),
                ('isCompleted', models.BooleanField()),
            ],
            options={
                'unique_together': {('title', 'time')},
            },
        ),
    ]

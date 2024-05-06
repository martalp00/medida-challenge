# Generated by Django 5.0.5 on 2024-05-06 20:50

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('eventId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('eventDate', models.DateField()),
                ('eventTime', models.TimeField()),
                ('homeTeamId', models.UUIDField()),
                ('homeTeamNickName', models.CharField(max_length=255)),
                ('homeTeamCity', models.CharField(max_length=255)),
                ('homeTeamRank', models.PositiveIntegerField(default=1)),
                ('homeTeamRankPoints', models.FloatField(default=0.0)),
                ('awayTeamId', models.UUIDField()),
                ('awayTeamNickName', models.CharField(max_length=255)),
                ('awayTeamCity', models.CharField(max_length=255)),
                ('awayTeamRank', models.PositiveIntegerField(default=1)),
                ('awayTeamRankPoints', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='EventsRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('league', models.CharField(choices=[('NFL', 'NFL')], max_length=10)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='EventsResponse',
            fields=[
                ('eventId', models.UUIDField(primary_key=True, serialize=False)),
                ('eventDate', models.DateField()),
                ('eventTime', models.TimeField()),
                ('homeTeamId', models.UUIDField()),
                ('homeTeamNickName', models.CharField(max_length=255)),
                ('homeTeamCity', models.CharField(max_length=255)),
                ('homeTeamRank', models.PositiveIntegerField(default=1)),
                ('homeTeamRankPoints', models.FloatField(default=0.0)),
                ('awayTeamId', models.UUIDField()),
                ('awayTeamNickName', models.CharField(max_length=255)),
                ('awayTeamCity', models.CharField(max_length=255)),
                ('awayTeamRank', models.PositiveIntegerField(default=1)),
                ('awayTeamRankPoints', models.FloatField(default=0.0)),
            ],
        ),
    ]
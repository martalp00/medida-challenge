from django.db import models
from enum import Enum
import uuid

# Create your models here.

class LeagueEnum(Enum):
    NFL = 'NFL'

class EventsRequest(models.Model):
    LEAGUE_CHOICES = [(league.value, league.name) for league in LeagueEnum]

    league = models.CharField(max_length=10, choices=LEAGUE_CHOICES)
    startDate = models.DateField()
    endDate = models.DateField()

class EventsResponse(models.Model):
    eventId = models.UUIDField(primary_key=True)
    eventDate = models.DateField()
    eventTime = models.TimeField()
    homeTeamId = models.UUIDField()
    homeTeamNickName = models.CharField(max_length=255)
    homeTeamCity = models.CharField(max_length=255)
    homeTeamRank = models.PositiveIntegerField(default=1)
    homeTeamRankPoints = models.FloatField(default=0.0)
    awayTeamId = models.UUIDField()
    awayTeamNickName = models.CharField(max_length=255)
    awayTeamCity = models.CharField(max_length=255)
    awayTeamRank = models.PositiveIntegerField(default=1)
    awayTeamRankPoints = models.FloatField(default=0.0)

class Event(models.Model):
    eventId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    eventDate = models.DateField()
    eventTime = models.TimeField()
    homeTeamId = models.UUIDField()
    homeTeamNickName = models.CharField(max_length=255)
    homeTeamCity = models.CharField(max_length=255)
    homeTeamRank = models.PositiveIntegerField(default=1)
    homeTeamRankPoints = models.FloatField(default=0.0)
    awayTeamId = models.UUIDField()
    awayTeamNickName = models.CharField(max_length=255)
    awayTeamCity = models.CharField(max_length=255)
    awayTeamRank = models.PositiveIntegerField(default=1)
    awayTeamRankPoints = models.FloatField(default=0.0)

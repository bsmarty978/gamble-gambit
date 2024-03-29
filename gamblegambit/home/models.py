from django.db import models

# Create your models here.
# class Roster(models.Model):
#     team_a_name = models.CharField(max_length=10)
#     team_b_name = models.CharField(max_length=10)
    
class Matches(models.Model):
    title = models.CharField(max_length=30)
    team_a = models.CharField(max_length=10)
    team_b = models.CharField(max_length=10)
    team_a_flag = models.URLField(blank=True, null=True)
    team_b_flag = models.URLField(blank=True, null=True)
    game = models.CharField(max_length=20)
    competation = models.CharField(max_length=20,blank=True, null=True)
  
    time = models.CharField(max_length=20)
    time_obj = models.DateTimeField()
    # roster = models.ForeignKey(Roster,on_delete=models.CASCADE)
    # this field can be uncommented if photos are available
    # roster = models.JSONField()
    # photos = models.JSONField()
    # team_a_photos = models.JSONField()
    # team_b_photos = models.JSONField()
    # country = models.CharField(max_length=20, blank=True, null=True)
    roster = models.JSONField(blank=True, null=True)
    result = models.JSONField(blank=True, null=True)
    photos = models.JSONField(blank=True, null=True)
    isUpcoming = models.BooleanField()
    isOngoiing = models.BooleanField()
    isCompleted = models.BooleanField()
    class Meta:
        unique_together = ["title", "time", "game"]

    def __str__(self):
        return self.title

class UpcomingMatchesList(models.Model):
    pass


class RsixPlayerList(models.Model):
    name = models.CharField(max_length=10)
    rating = models.FloatField()
    totalmatch = models.IntegerField()
    
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    data = models.TextField()
    chance1 = models.BooleanField(default=False)
    chance2 = models.BooleanField(default=False)
    time1 = models.IntegerField(default=900000)
    time2 = models.IntegerField(default=900000)
    # state = models.IntegerField(default=-1)
    lastTime = models.BigIntegerField()
    move = models.IntegerField(default=1)

class UserE(models.Model):
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

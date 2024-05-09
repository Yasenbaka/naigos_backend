from django.db import models


# Create your models here.

class Users(models.Model):
    qq_id = models.BigIntegerField()
    register_group = models.BigIntegerField()
    nickname = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    favorite = models.IntegerField(default=0)
    avatar = models.URLField()
    channel_user_id = models.CharField(max_length=255)

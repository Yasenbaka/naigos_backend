from django.db import models


# Create your models here.

class Bots(models.Model):
    bot_appid = models.BigIntegerField()
    access_token = models.TextField()
    refresh_token = models.TextField()
    safe_level = models.IntegerField(default=10)

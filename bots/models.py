from django.db import models


# Create your models here.

class Bots(models.Model):
    bot_appid = models.BigIntegerField()
    token = models.TextField(default='token')
    password = models.TextField(default='<PASSWORD>')
    safe_level = models.IntegerField(default=10)

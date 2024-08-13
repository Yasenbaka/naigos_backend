import uuid
from django.db import models


# Create your models here.

class Users(models.Model):
    qq_id = models.BigIntegerField(default='请尽快绑定QQ号~')
    group_real_user_id = models.CharField(max_length=100)
    register_real_group_id = models.CharField(max_length=100)
    nickname = models.CharField(max_length=255, default='请尽快更名~')
    city = models.CharField(max_length=100, default='unknown')
    score = models.IntegerField(default=0)
    favorite = models.IntegerField(default=50)
    avatar = models.URLField(default='https://naigos.cn/images/108202018_p3.jpg')
    email = models.EmailField(
        default='绑定邮箱或申请奶果邮@naigos.cn',
        null=False,
        blank=False
    )
    safe_level = models.IntegerField(default=10)


class Password(models.Model):
    uuid = models.UUIDField()
    password = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=6, null=True, blank=True)
    is_code = models.BooleanField(default=False)
    expiration_date = models.BigIntegerField(null=True, blank=True)


class Judges(models.Model):
    qq_id = models.CharField(max_length=255)
    score = models.CharField(max_length=8, default=20080101)
    favorite = models.CharField(max_length=8, default=20080101)
    transfer_archive = models.BooleanField(default=False)

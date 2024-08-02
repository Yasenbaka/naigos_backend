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


class Judges(models.Model):
    qq_id = models.CharField(max_length=255)
    score = models.CharField(max_length=8, default=20080101)
    favorite = models.CharField(max_length=8, default=20080101)
    transfer_archive = models.BooleanField(default=False)

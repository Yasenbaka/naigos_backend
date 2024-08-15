from django.db import models

# Create your models here.


class SogouInputTheme(models.Model):
    theme_id = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255)
    introduce = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    header_image = models.URLField(blank=True, null=True)
    eject_image = models.URLField(blank=True, null=True)
    details_image = models.URLField(blank=True, null=True)
    cost = models.IntegerField(default=100)

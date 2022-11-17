from django.db import models
from six import python_2_unicode_compatible


# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=10, verbose_name='名字', null=True, blank=True)
    password = models.CharField(max_length=16, verbose_name='密码', null=True, blank=True)

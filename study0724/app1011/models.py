from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=8, verbose_name='用户名')
    password = models.CharField(max_length=16, verbose_name='密码')
    create_time = models.DateTimeField(auto_now=True, blank=False, null=False, verbose_name='创建时间')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'


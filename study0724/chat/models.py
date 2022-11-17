from django.db import models


# Create your models here.


class Chat(models.Model):
    username = models.CharField(max_length=12, verbose_name='用户名')
    message = models.CharField(max_length=100, verbose_name='聊天内容')
    send_message_time = models.DateTimeField(auto_now_add=True, verbose_name='信息发送时间', editable=False)

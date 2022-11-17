# encoding: utf-8

"""
@python_version: python3.7.2
@author: ran.ao
@contact: ran.ao@daocloud.io
@software: PyCharm
@file: routing.py
@time: 2022/10/21 -10:56
@file_version:
@describe:

"""
# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]

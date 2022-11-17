# encoding: utf-8

"""
@python_version: python3.7.2
@author: ran.ao
@contact: ran.ao@daocloud.io
@software: PyCharm
@file: urls.py
@time: 2022/10/20 -17:23
@file_version:
@describe:

"""
from django.conf.urls import url, include
from django.urls import path

from .views import hello, index,room

urlpatterns = [
    path('hello/', hello),
    path('', index, name='index'),
    path("<str:room_name>/", room, name="room"),
]

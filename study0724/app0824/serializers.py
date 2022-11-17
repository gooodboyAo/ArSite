# encoding: utf-8

"""
@python_version: python3.7.2
@author: ran.ao
@contact: ran.ao@daocloud.io
@software: PyCharm
@file: serializers.py
@time: 2022/8/24 -14:57
@file_version:
@describe:

"""
from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



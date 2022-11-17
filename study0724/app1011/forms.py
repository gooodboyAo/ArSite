# encoding: utf-8

"""
@python_version: python3.7.2
@author: ran.ao
@contact: ran.ao@daocloud.io
@software: PyCharm
@file: forms.py
@time: 2022/10/13 -17:11
@file_version:
@describe:

"""
from django import forms
from captcha.fields import CaptchaField


class CaptchaForm(forms.Form):
    captcha = CaptchaField()

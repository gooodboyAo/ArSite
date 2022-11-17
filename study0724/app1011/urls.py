# encoding: utf-8

"""
@python_version: python3.7.2
@author: ran.ao
@contact: ran.ao@daocloud.io
@software: PyCharm
@file: urls.py
@time: 2022/10/11 -14:19
@file_version:
@describe:

"""
from django.urls import path
from app1011 import views
from django.conf.urls import include
from django.views.generic import RedirectView

urlpatterns = [
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('login/captcha/', include('captcha.urls')),
    path('login/email/', views.send_message)
    # path('login/', views.LoginView.as_view()),

]

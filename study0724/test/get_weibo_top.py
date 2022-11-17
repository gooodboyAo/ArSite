"""
@python_version: python3.7.2
@author: ran.ao
@contact: ran.ao@daocloud.io
@software: PyCharm
@file: get_weibo_top.py
@time: 2022/8/3 -10:17
@file_version:
@describe:

"""
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time, re
import os

# 配置模拟浏览器的位置
headers = {
    "UserAgent": "",
    "cooke": '',
}
data = requests.get('https://www.baidu.com')
data.encoding = data.apparent_encoding
print(data.text)

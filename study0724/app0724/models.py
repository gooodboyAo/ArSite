# encoding: utf-8
import time

from django.db import models
import uuid
import datetime


class Department(models.Model):
    '''
    部门表
    '''
    title = models.CharField(verbose_name='标题', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    '''
    员工表
    '''
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    # 账户余额 总长10  小数点长度2 默认为0
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name='入职时间')

    # 关联表
    # 级联删除
    depart = models.ForeignKey(to="Department", to_field='id', on_delete=models.CASCADE, verbose_name='部门')
    # 允许为空 设置为空
    # depart = models.ForeignKey(to="Department", to_field='id', null=True, blank=True, on_delete=models.SET_NULL)

    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)


class GoodMobileNumber(models.Model):
    """ 靓号表"""
    mobile = models.CharField(max_length=12, verbose_name='手机号')
    price = models.DecimalField(verbose_name='价格', max_digits=10, decimal_places=2, default=0)

    level_choices = (
        (1, '一级'),
        (2, '二级'),
        (3, '三级'),
        (4, '四级'),
        (5, '五级'),
    )
    level = models.SmallIntegerField(verbose_name='账号级别', choices=level_choices, default=2)

    status_choices = (
        (1, '已占用'),
        (2, '未占用')
    )
    status = models.SmallIntegerField(verbose_name="", choices=status_choices, default=2)


# 格式上传文件的文件名
def image_upload_to(instance, filename):  # 文件的时间戳
    id = time.strftime('"%Y%m%d%H%M%S"', time.localtime(time.time()))
    filename = 'upload_' + str(filename).split('.')[0] + '_' + id + '.' + str(filename).split('.')[-1]
    # print(filename)
    return 'file/+{filename}'.format(uuid=uuid.uuid4().hex, filename=filename)


class FileUpload(models.Model):
    """上传文件类"""
    # 'file/' 上传文件路径media/file 不允许为空
    file_name = models.FileField(upload_to=image_upload_to, blank=False, null=False)
    # 上传时间
    upload_time = models.DateTimeField(auto_now_add=True)
    # 下载时间
    download_time = models.DateTimeField(blank=True, null=True)


class Microservice(models.Model):
    microservice_name = models.CharField(verbose_name='服务名称', max_length=32)
    microservice_desc = models.CharField(verbose_name='服务备注', max_length=200)
    create_time = models.DateTimeField(auto_now=True, verbose_name='服务创建时间')
    is_running_choices = (
        (0, '未运行'),
        (1, '正在运行'),
    )
    is_running = models.SmallIntegerField(choices=is_running_choices, verbose_name='是否在运行', default=0)

    is_delete_choices = (
        (0, '未删除'),
        (1, '已删除'),
    )
    is_delete = models.SmallIntegerField(choices=is_delete_choices, verbose_name='是否删除', default=0)
    delete_time = models.DateTimeField(auto_now=True, verbose_name="删除时间")

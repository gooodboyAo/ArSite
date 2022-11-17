import json
import os.path

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, FileResponse, StreamingHttpResponse, JsonResponse
from django.utils.safestring import mark_safe

from app0724 import models
from django import forms
from django.core.validators import RegexValidator, ValidationError
from django.conf import settings
import time


# Create your views here.


def depart_list(request):
    ''' 部门列表 '''
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    ''' 添加部门 '''
    if request.method == "GET":
        return render(request, 'depart_add.html')
    title = request.POST.get('title')
    models.Department.objects.create(title=title)
    return redirect('/department/list/')


def depart_delete(request):
    # 获取ID
    nid = request.GET.get('nid')
    # 删除
    models.Department.objects.filter(id=nid).delete()
    # 重定向
    return redirect('/department/list/')


def depart_edit(request, nid):
    if request.method == "GET":
        row_info = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'row_info': row_info})
    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/department/list/')


def user_list(request):
    """ 用户列表 """
    user_info = models.UserInfo.objects.all()
    return render(request, 'user_list.html', {"user_info": user_info})


def user_add(request):
    """ 添加用户 原始方法"""
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('account')
    ctime = request.POST.get('ctime')
    depart_id = request.POST.get('depart')
    gender = request.POST.get('gender')

    models.UserInfo.objects.create(name=user, password=pwd, age=age, account=account, create_time=ctime,
                                   depart_id=depart_id, gender=gender)

    return redirect('/user/list/')


# modelform 添加用户
# model form
class UserModelForm(forms.ModelForm):
    name = forms.CharField(max_length=12, label='用户名')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = models.UserInfo
        # 所有字段
        # fields = '__all__'
        # 自定义字段
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']

        # widgets = {
        #     'name': forms.TextInput(attrs={"class": "form-control"})
        # }


def user_model_add(request):
    """添加用户"""
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})
    # 用户提交post 校验数据 校验成功
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')

    return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, uid):
    # 用户编辑
    row_obj = models.UserInfo.objects.filter(id=uid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row_obj)
        return render(request, 'user_edit.html', {"form": form})
    form = UserModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        # 默认输入的是用户输入的所有值  如果想改变其他值
        # form.instance.字段名 == xxx
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, uid):
    models.UserInfo.objects.filter(id=uid).delete()
    return redirect('/user/list/')


def goodnumber_list(request):
    # # 根据级别排序
    # for i in range(303):
    #     models.GoodMobileNumber.objects.create(mobile='15187829296',price=10,level=1,status=1)
    data_dict = {}
    search_data = request.GET.get('gs', "")  # /?q=77 通过q传递筛选参数；q有值拿值 ，没值为空
    if search_data:  # q为空的话，data_dict为空，filter(**data_dict)相当于all()
        data_dict["mobile__contains"] = search_data

    page = int(request.GET.get('page'))
    page_size = 10
    start, end = (page - 1) * page_size, page * page_size

    page_str_list = []
    for i in range(1, 10):
        page_str_list.append('<li><a href="?page={}">{}</a></li>'.format(i, i))
    page_str = mark_safe("".join(page_str_list))


    # **data_dict : 能查询到结果就显示结果 如果没有结果就显示全部（没有查询结果）
    pretty_list = models.GoodMobileNumber.objects.filter(**data_dict).order_by("-level")[start:end]
    return render(request, 'goodnumber_list.html',
                  {'number_info': pretty_list, 'search_data': search_data, 'page_str': page_str})
    # {'search_data': search_data}传参是为了在搜索框里显示上次结果

    # number_info = models.GoodMobileNumber.objects.all().order_by('-level')
    # return render(request, 'goodnumber_list.html', {"number_info": number_info})


class GoodNumberForm(forms.ModelForm):
    # 校验手机号 方式1
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'1[3-9]\d{9}$', '手机号格式错误')]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = models.GoodMobileNumber
        fields = ['mobile', 'price', 'level', 'status']
        # 排除哪个字段
        exclude = []

    # 手动校验手机号 方式2
    # clean_字段名
    def clean_mobile(self):
        # 获取用户输入信息 -手机号
        text_mobile = self.cleaned_data['mobile']
        if models.GoodMobileNumber.objects.filter(mobile=text_mobile).exists():
            # 验证不通过
            raise ValidationError("手机已经存在")
        # 验证通过返回值
        return text_mobile


def goodnumber_add(request):
    if request.method == 'GET':
        form = GoodNumberForm()
        return render(request, 'goodnumber_add.html', {"form": form})
    form = GoodNumberForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/goodnumber/list/')
    return render(request, 'goodnumber_add.html', {"form": form})


def welcome(request):
    return render(request, 'welcome.html')


def uploadFileSubmit(request):
    if request.method == 'GET':
        return render(request, 'upload_file.html', {'message': ''})
    file = request.FILES.get('file_name')
    try:
        if file:
            models.FileUpload.objects.create(file_name=file)
            return redirect('/file/list/')
        else:
            return render(request, 'upload_file.html',
                          {'message': '上传失败'})
    except Exception as e:
        print(e)
        # 2.使用模板
        return render(request, 'upload_file.html',
                      {'message': '上传失败'})


def file_list(request):
    if request.method == "GET":
        filelist = models.FileUpload.objects.all()
        return render(request, 'file_list.html', {'file_list': filelist})


def file_delete(request, f_id):
    models.FileUpload.objects.filter(id=f_id).delete()
    return redirect('/file/list/')


def file_download(request, f_id):
    file_name = models.FileUpload.objects.filter(id=f_id).values()[0].get('file_name')
    try:
        response = StreamingHttpResponse(open(os.path.join(settings.MEDIA_ROOT, file_name), 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(
            os.path.join(settings.MEDIA_ROOT, file_name))
        return response
    except Exception:
        raise Http404


def map_show(request):
    return render(request, 'china_map.html')


class GoodNumberEditForm(forms.ModelForm):
    # 校验手机号 方式1
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'1[3-9]\d{9}$', '手机号格式错误')]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = models.GoodMobileNumber
        fields = ['mobile', 'price', 'level', 'status']
        # 排除哪个字段
        exclude = []

    # 手动校验手机号 方式2
    # clean_字段名
    def clean_mobile(self):
        # 获取用户输入信息 -手机号
        text_mobile = self.cleaned_data['mobile']
        # 排除自己ID 除外的数据
        if models.GoodMobileNumber.objects.exclude(id=self.instance.pk).filter(mobile=text_mobile).exists():
            raise ValidationError("手机号已经存在")
        # 验证通过返回值
        return text_mobile


def goodnumber_edit(request, nid):
    row_obj = models.GoodMobileNumber.objects.filter(id=nid).first()
    if request.method == "GET":
        form = GoodNumberEditForm(instance=row_obj)
        return render(request, 'goodnumber_edit.html', {"form": form})
    form = GoodNumberEditForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        # 默认输入的是用户输入的所有值  如果想改变其他值
        # form.instance.字段名 == xxx
        form.save()
        return redirect('/goodnumber/list/')
    return render(request, 'goodnumber_edit.html', {"form": form})


def goodnumber_delete(request, nid):
    models.GoodMobileNumber.objects.filter(id=nid).delete()
    return redirect('/goodnumber/list/')


# class MicroServiceModelForm(forms.ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs = {"class": "form-control"}
#
#     class Meta:
#         model = models.Microservice
#         fields = ['microservice_name', 'microservice_desc', 'create_time', 'is_running']
#         exclude = []
#
#     def clean_microservice_name(self):
#         # microservice_name校验
#         pass


def microservice_list(request):
    # 获取当前文件路径
    micro_info = {}
    for i in os.listdir(settings.MICROSERVICES_URL):
        micro_info[i] = [i.split('.')[0], time.strftime('%Y-%m-%d %H:%M:%S',
                                                        time.localtime(os.path.getctime(
                                                            os.path.join(settings.MICROSERVICES_URL, i))))]
    return render(request, 'microservices_list.html', {"data": micro_info})


def microservice_add(request):
    if request.method == 'GET':
        return render(request, 'microservices_add.html', {'error_msg': ""})
    name = request.POST.get('microservicename')
    if name in [i.split('.'[0]) for i in os.listdir(settings.MICROSERVICES_URL)]:
        return render(request, 'microservices_add.html', {'error_msg': "服务已存在"})
    content = settings.MICROSERVICES_URL + "/" + '{}.py'.format(name)
    with open(content, 'w+') as f:
        f.read()
    return redirect('/microservices/list/')


def microservice_start(request, m_name):
    microservice_name = m_name
    print(microservice_name)
    return HttpResponse('服务启动')


def get_ajax(request):
    print('加载页面')
    print(request.method)

    if request.is_ajax():
        print(request.body)
        print(request.POST)
        name = request.POST.get('username')
        password = request.POST.get("password")
        print(name)
        print(password)

        if name == '123' and password == '123':
            ret = {'msg': '用户名正确'}
        else:
            ret = {'msg': "用户名密码错误"}
        return HttpResponse(json.dumps(ret))
    else:
        return render(request, 'ajax_test.html', {'msg': "用户名密码错误"})

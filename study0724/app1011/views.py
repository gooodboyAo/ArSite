from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.views import View
from app1011 import models


def index(request):
    return render(request, 'index.html')


def send_message(request):
    if request.is_ajax():
        # 前端界面数据
        print(request.POST)
        # {'name': ['as'], 'email': ['as'], 'msg_subject': ['sa'], 'message': ['as']}
        print()
    return JsonResponse({"text": 'success'})


# def login(request):
#     hashkey = CaptchaStore.generate_key()
#     image_url =captcha_image_url(hashkey)
#     vcode_key = request.POST.get('hashkey')
#     get_captach = CaptchaStore.objects.get(hashkey=vcode_key)
#     if request.method == "GET":
#         return render(request, 'login.html', {"msg_info": ''})
#     user_name = request.POST.get('loginInfo.nick')
#     password = request.POST.get('loginInfo.nick')
#     if user_name == 'root' and password == 'root':
#         return HttpResponse('登录成功')
#     # return render(request, 'login.html', {"msg_info": '账号密码错误'})
def refresh_vcode(request):
    return render(request, 'login.html', locals())


def login(request):
    # 验证码生成
    hashkey = CaptchaStore.generate_key()
    imgage_url = captcha_image_url(hashkey)

    if request.method == 'POST':
        # 用户名
        username = request.POST.get('loginInfo.nick')
        # 密码
        password = request.POST.get('loginInfo.password')
        # 用户输入验证码
        vcode = request.POST.get('vcode')
        vcode_key = request.POST.get('hashkey')
        # 验证查询数据库生成正确的码
        get_captcha = CaptchaStore.objects.get(hashkey=vcode_key)
        print(username, password, get_captcha)
        try:
            user = models.User.objects.get(username=username)
        except:
            message = '用户不存在！'
            return render(request, 'login.html', locals())

        if user.password == password:
            # 将用户输入值小写后与数据库查询的response值对比：
            if vcode.lower() == get_captcha.response:
                return redirect('/user/list/')
            else:
                message = '验证码不正确！'
                return render(request, 'login.html', locals())
        else:
            message = '密码不正确！'
            return render(request, 'login.html', locals())
    else:
        return render(request, 'login.html', locals())


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    return HttpResponse('提交注册界面')


class LoginView(View):
    def get(self, request):
        from .forms import CaptchaForm
        captcha_form = CaptchaForm()
        print(captcha_form.fields)
        return render(request, 'login.html', {'captcha_form': captcha_form})

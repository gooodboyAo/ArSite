from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic.base import TemplateView

from . import views

# router = DefaultRouter()  # 可以处理视图的路由器
# router.register(r'user', views.UserInfoViewSet)  # 向路由器中注册视图集

urlpatterns = [
    # path('', views.toLogin),
    path('', views.home, name='logout'),
    # path('login/', views.login, name='namelogin'),
    path('hello/', views.hello, name='login'),
    # get
    # url("^user/(?P<pk>[0-9]+)/$", views.getuser, name="getuser"),
    # url("user/list_all/", views.UserInfoViewSet.as_view({'get': "list"})),
    url("user/list_all/", TemplateView.as_view(template_name='i')),
    url("^user/list_one/(?P<pk>[0-9]+)/$", views.getuser, name="getuser"),
    url("^user/update/(?P<pk>[0-9]+)/$", views.update_info, name="updateinfo")

]

# urlpatterns += router.urls

"""study0724 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app0724 import views
from app1011 import views as view_1
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  # 文件上传路径
                  # path('echart/', include('smart_chart.echart.urls')),
                  # path(r'', RedirectView.as_view(url='echart/index/')),

                  path('0824/', include('app0824.urls')),
                  path('1011/', include('app1011.urls')),
                  path('chat/', include('chat.urls')),
                  url(r'file/upload/', views.uploadFileSubmit),

                  url(r'main', view_1.index),
                  # 部门管理
                  path('department/list/', views.depart_list),
                  path('department/add/', views.depart_add),
                  path('department/delete/', views.depart_delete),
                  path("department/<int:nid>/edit/", views.depart_edit),

                  # 用户管理
                  path('user/list/', views.user_list),
                  path('user/add/', views.user_add),
                  path('user/model/form/add', views.user_model_add),
                  # 编辑用户  基于modelform
                  path('user/<int:uid>/edit/', views.user_edit),
                  path('user/<int:uid>/delete/', views.user_delete),

                  # 靓号管理
                  path('goodnumber/list/', views.goodnumber_list),
                  path('goodnumber/add/', views.goodnumber_add),
                  path('goodnumber/<int:nid>/edit/', views.goodnumber_edit),
                  path('goodnumber/<int:nid>/delete/', views.goodnumber_delete),
                  # 文件相关
                  path('file/list/', views.file_list),
                  path('file/<int:f_id>/delete/', views.file_delete),
                  path('file/<int:f_id>/download/', views.file_download),

                  path('map/show/', views.map_show),

                  path('microservices/list/', views.microservice_list),
                  path('microservices/add/', views.microservice_add),
                  path('microservices/<str:m_name>/start/', views.microservice_start),

                  path('ajax/test/', views.get_ajax)

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

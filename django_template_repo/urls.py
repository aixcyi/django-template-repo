"""
django_template_repo 项目的根路由配置。

``urlpatterns`` 是一个 Django 固定的变量名，它包含指向视图的 URL 配置。详见话题
`URL调度器 <https://docs.djangoproject.com/zh-hans/5.2/topics/http/urls/>`_
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

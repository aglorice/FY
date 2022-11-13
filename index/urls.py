# -*- coding = utf-8 -*-
# @Time :2022/11/11 22:15
# @Author :小岳
# @Email  :401208941@qq.com
# @PROJECT_NAME :djangoProject1
# @File :  urls.py
from django.urls import path

from index import views

urlpatterns = [
    path('', views.index)  # 返回每个区域的数量
]
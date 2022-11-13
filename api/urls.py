# -*- coding = utf-8 -*-
# @Time :2022/11/11 21:25
# @Author :小岳
# @Email  :401208941@qq.com
# @PROJECT_NAME :djangoProject1
# @File :  urls.py
from django.urls import path

from api import views

urlpatterns = [
    path('getareadata/', views.getareadata),  # 返回每个区域的数量
    path('getall/', views.getall),  # 返回所有的数据
    path('update/', views.update),  # 更新数据
]

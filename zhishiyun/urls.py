"""zhishiyun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path

from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 学习空间路由，无参数代表学习空间目录，有第一个参数且为数字代表该学习空间主页，为new则代表创建学习空间界面
    # 有前两个代表该学习空间某元素的主页，后面跟new则代表创建该元素页面，跟数字选择了某一元素观看
    path('spaces/', views.spaces_index),
    path("spaces/new/", views.space_create),
    re_path(r"^spaces/<int:space_id>/$", views.space_main),

    re_path(r"^spaces/<int:space_id>/resources/$", views.space_resources_index),
    re_path(r"^spaces/<int:space_id>/questions/$", views.space_questions_index),
    re_path(r"^spaces/<int:space_id>/exercises/$", views.space_exercises_index),
    re_path(r"^spaces/<int:space_id>/groups/$", views.space_groups_index),
    re_path(r"^spaces/<int:space_id>/notices/$", views.space_notices_index),

    re_path(r"^spaces/<int:space_id>/resources/<int:resources_id>/$", views.space_resources),
    re_path(r"^spaces/<int:space_id>/questions/<int:questions_id>/$", views.space_questions),
    re_path(r"^spaces/<int:space_id>/exercises/<int:exercises_id>/$", views.space_exercises),
    re_path(r"^spaces/<int:space_id>/groups/<int:groups_id>/$", views.space_groups),
    re_path(r"^spaces/<int:space_id>/notices/<int:notices_id>/$", views.space_notices),

    re_path(r"^spaces/<int:space_id>/resources/<int:resources_id>/edit/$", views.space_resources_create),
    re_path(r"^spaces/<int:space_id>/questions/<int:questions_id>/edit/$", views.space_questions_create),
    re_path(r"^spaces/<int:space_id>/exercises/<int:exercises_id>/edit/$", views.space_exercises_create),
    re_path(r"^spaces/<int:space_id>/groups/<int:groups_id>/edit/$", views.space_groups_create),
    re_path(r"^spaces/<int:space_id>/notices/<int:notices_id>/edit/$", views.space_notices_create),

    re_path(r"^spaces/<int:space_id>/resources/new/$", views.space_resources_create),
    re_path(r"^spaces/<int:space_id>/questions/new/$", views.space_questions_create),
    re_path(r"^spaces/<int:space_id>/exercises/new/$", views.space_exercises_create),
    re_path(r"^spaces/<int:space_id>/groups/new/$", views.space_groups_create),
    re_path(r"^spaces/<int:space_id>/notices/new/$", views.space_notices_create),
]

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
    path("spaces/<int:space_id>", views.space_main),

    path("spaces/<int:space_id>/resources", views.space_resources_index),
    path("spaces/<int:space_id>/questions", views.space_questions_index),
    path("spaces/<int:space_id>/exercises", views.space_exercises_index),
    path("spaces/<int:space_id>/groups", views.space_groups_index),
    path("spaces/<int:space_id>/notices", views.space_notices_index),

    path("spaces/<int:space_id>/resources/<int:resources_id>", views.space_resources),
    path("spaces/<int:space_id>/questions/<int:questions_id>", views.space_questions),
    path("spaces/<int:space_id>/exercises/<int:exercises_id>", views.space_exercises),
    path("spaces/<int:space_id>/groups/<int:groups_id>", views.space_groups),
    path("spaces/<int:space_id>/notices/<int:notices_id>", views.space_notices),

    path("spaces/<int:space_id>/resources/<int:resources_id>/edit", views.space_resources_edit),
    path("spaces/<int:space_id>/questions/<int:questions_id>/edit", views.space_questions_edit),
    path("spaces/<int:space_id>/exercises/<int:exercises_id>/edit", views.space_exercises_edit),
    path("spaces/<int:space_id>/groups/<int:groups_id>/edit", views.space_groups_edit),
    path("spaces/<int:space_id>/notices/<int:notices_id>/edit", views.space_notices_edit),

    path("spaces/<int:space_id>/resources/new", views.space_resources_create),
    path("spaces/<int:space_id>/questions/new", views.space_questions_create),
    path("spaces/<int:space_id>/exercises/new", views.space_exercises_create),
    path("spaces/<int:space_id>/groups/new", views.space_groups_create),
    path("spaces/<int:space_id>/notices/new", views.space_notices_create),

    path('register', views.register),  # 指定register函数的路由为register
    path('register/confirm', views.user_confirm),
    path('login', views.login),
    path('login/confirm', views.login_confirm),
    path('loginbyconfirm', views.login_by_confirm),
    path('logout', views.logout),
    path('changepassword', views.change_password),
    path('user/<uid>/', views.get_info),
    path('user/<uid>/edit', views.edit_info),
    path('user/activities', views.get_activities),
    path('user/<uid>/adminspaces', views.get_admin_spaces),
    path('user/<uid>/followspaces', views.get_follow_spaces),
    path('user/<uid>/resources', views.get_resources),
    path('user/<uid>/questions', views.get_questions),
    path('user/<uid>/answers', views.get_answers),
    path('user/<uid>/exercises', views.get_exercises),
    path('user/<uid>/collects/resources', views.get_collects_resources),
    path('user/<uid>/collects/questions', views.get_collects_questions),
    path('user/<uid>/collects/answers', views.get_collects_answers),
    path('user/<uid>/collects/exercises', views.get_collects_exercises),
    path('user/<uid>/followings', views.get_followings),
    path('user/<uid>/fans', views.get_fans),
    path('user/<uid>/follow', views.follow_people),
    path('file/<resource_id>', views.get_file_by_id),
    # path('postarticle', postarticle),
     path('search',views.search),
    path('give',views.give_uid)
]

from django.urls import path
from .views import *

urlpatterns = [
    path('register', register),  # 指定register函数的路由为register
    path('register/confirm', user_confirm),
    path('login', login),
    path('logout', logout),
    path('changepassword', change_password),
    path('user/<uid>/', get_info),
    path('user/<uid>/edit', edit_info),
    path('user/<uid>/activities', get_activities),
    path('user/<uid>/adminspaces', get_admin_spaces),
    path('user/<uid>/followspaces', get_follow_spaces),
    path('user/<uid>/resources', get_resources),
    path('user/<uid>/questions', get_questions),
    path('user/<uid>/exercises', get_exercises),
    path('user/<uid>/collects/resources', get_collects_resources),
    path('user/<uid>/collects/questions', get_collects_questions),
    path('user/<uid>/collects/answers', get_collects_answers),
    path('user/<uid>/collects/exercises', get_collects_exercises),
    path('user/<uid>/followings', get_followings),
    path('user/<uid>/fans', get_fans),
    path('user/<uid>/follow', follow_people),
    # path('postarticle', postarticle),
    # path('search',search)
]

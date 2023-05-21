from django.urls import path
from .views import *

urlpatterns = [
    path('register', register),  # 指定register函数的路由为register
    path('register/confirm', user_confirm),
    path('login', login),
    path('logout', logout),
    path('user/<uid>/', get_info),
    path('user/<uid>/edit', edit_info),
    path('user/<uid>/activities', get_activities),
    path('user/<uid>/edit', edit_info),
    # path('postarticle', postarticle),
    # path('search',search)
]

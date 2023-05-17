from django.urls import path
from .views import *

urlpatterns = [
    path('register', register),  # 指定register函数的路由为register
    path('confirm/email', user_confirm),
    # path('login', login),
    # path('logout', logout),
    # path('postarticle', postarticle),
    # path('search',search)
]

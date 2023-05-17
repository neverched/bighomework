import json

import re
from django.http import JsonResponse
from django.shortcuts import render

import requests
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from app01.models import User, Mails
from tools.emails import *
from pytz import utc


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = json.loads(request.body)['username']
        password1 = json.loads(request.body)['password1']
        password2 = json.loads(request.body)['password2']
        email = json.loads(request.body)['email']

        user_exist = User.objects.filter(username=username)

        if user_exist:
            return JsonResponse({'error': 1002, 'msg': '用户名已存在!'})

        email_exist = User.objects.filter(email=email)

        if email_exist:
            return JsonResponse({'error': 1003, 'msg': '邮箱已存在!'})

        # 检查密码，要求：8-18字符，英文字母+数字
        if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', password1):
            return JsonResponse({'error': 1004, 'msg': '密码不合格!'})

        if password2 != password1:
            return JsonResponse({'error': 1005, 'msg': '两次输入密码不一致!'})

        new_user = User()
        new_user.username = username
        new_user.password = password1
        new_user.email = email
        new_user.intro = "我们走，学报"
        new_user.save()

        code = make_confirm_string(new_user)
        try:
            send_email_confirm(email, code)
        except:
            new_user.delete()
            return JsonResponse({'error': 1006, 'msg': '验证邮件发送失败，请稍后再试!'})

        return JsonResponse({'error': 1, 'msg': '注册成功'})
    else:
        return JsonResponse({'error': 1001, 'msg': "请求方式错误"})
        # user1 =


@csrf_exempt
def user_confirm(request):
    if request.method == 'POST':
        code = json.loads(request.body)['code']
        try:
            confirm = ConfirmString.objects.get(code=code)
        except:
            return JsonResponse({'error': 2002, 'msg': "没有确认邮件"})
        c_time = confirm.c_time.replace(tzinfo=utc)
        now = datetime.datetime.now().replace(tzinfo=utc)
        if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
            confirm.user.delete()
            return JsonResponse({'error': 2003, 'msg': "确认邮件已过期"})
        else:
            confirm.user.has_confirmed = True
            confirm.user.save()
            confirm.delete()
            return JsonResponse({'error': 1, 'msg': "验证成功"})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})

import datetime
import json
import re

from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from pytz import utc

from app01.models import User
from tools.emails import *


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
            return JsonResponse({'error': 2002, 'msg': "验证码错误"})
        c_time = confirm.c_time.replace(tzinfo=utc)
        now = datetime.datetime.now().replace(tzinfo=utc)
        if now > c_time + datetime.timedelta(3):
            confirm.user.delete()
            return JsonResponse({'error': 2003, 'msg': "确认邮件已过期"})
        else:

            confirm.user.confirmed = True
            confirm.user.save()
            confirm.delete()
            return JsonResponse({'error': 1, 'msg': "验证成功"})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # 获取请求数据
        password = request.POST.get('password')
        if request.session.get('username') == username:
            return JsonResponse({'error': 1009, 'msg': "已经登录"})
        user = User.objects.get(username=username)
        if user.password == password:  # 判断请求的密码是否与数据库存储的密码相同
            if not user.confirmed:
                return JsonResponse({'error': 1010, 'msg': "未确认"})
            request.session['username'] = username  # 密码正确则将用户名存储于session（django用于存储登录信息的数据库位置）
            return JsonResponse({'error': 1, 'msg': "登录成功"})
        else:
            return JsonResponse({'error': 1002, 'msg': "密码错误"})
    else:
        return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def logout(request):
    request.session.flush()
    return JsonResponse({'errno': 0, 'msg': "注销成功"})

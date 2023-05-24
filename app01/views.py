import datetime
import json
import re

from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from pytz import utc

from app01.models import *
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
        username = json.loads(request.body)['username']  # 获取请求数据
        password = json.loads(request.body)['password']
        if request.session.get('username') == username:
            return JsonResponse({'error': 1009, 'msg': "已经登录"})
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({'error': 1011, 'msg': "没有此用户"})
        if user.password == password:  # 判断请求的密码是否与数据库存储的密码相同
            if not user.confirmed:
                return JsonResponse({'error': 1010, 'msg': "未确认"})
            request.session['uid'] = user.id  # 密码正确则将用户名存储于session（django用于存储登录信息的数据库位置）
            return JsonResponse({'error': 1, 'msg': "登录成功"})
        else:
            return JsonResponse({'error': 1002, 'msg': "密码错误"})
    else:
        return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def logout(request):
    request.session.flush()
    return JsonResponse({'error': 1, 'msg': "注销成功"})


@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        username = json.loads(request.body)['username']
        old_password = json.loads(request.body)['password']
        password1 = json.loads(request.body)['password1']
        password2 = json.loads(request.body)['password2']
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({'error': 1011, 'msg': "没有此用户"})
        if user.password == old_password:
            if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', password1):
                return JsonResponse({'error': 1004, 'msg': '密码不合格!'})
            if password1 != password2:
                return JsonResponse({'error': 1005, 'msg': '两次输入密码不一致!'})
            user.password = password1
            user.save()
            return JsonResponse({'error': 1, 'msg': "密码修改成功"})
        else:
            return JsonResponse({'error': 1002, 'msg': "密码错误"})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def get_info(request, uid):
    if request.method == 'GET':
        uid = int(uid)
        try:
            user = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1011, 'msg': "没有此用户"})
        return JsonResponse(
            {'error': 1, 'msg': '查找信息成功', 'username': user.username, 'gender': user.gender, 'tags': user.tags,
             'destination': user.destination,
             'job': user.job, 'organization': user.organization, 'intro': user.intro,
             'followers': user.followers, 'followings': user.followings, 'like': user.like})

    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def edit_info(request, uid):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})

        try:
            user_id = request.session['uid']
        except:
            return JsonResponse({'error': 1014, 'msg': "没有登录"})
        if user_id != int(uid):
            return JsonResponse({'error': 1012, 'msg': "这不是你的空间哦"})

        username = json.loads(request.body)['username']
        gender = json.loads(request.body)['gender']
        tags = json.loads(request.body)['tags']
        destination = json.loads(request.body)['destination']
        job = json.loads(request.body)['job']
        organization = json.loads(request.body)['organization']
        intro = json.loads(request.body)['intro']

        user.username = username
        user.gender = gender
        user.tags = tags
        user.destination = destination
        user.job = job
        user.organization = organization
        user.intro = intro
        user.save()

        return JsonResponse({'error': 1, 'msg': '更新信息成功'})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def get_activities(request):
    if request.method == 'GET':
        uid = request.session.get('uid')
        try:
            follow = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})
        try:
            activities = Activities.objects.filter(hosts=uid)
        except:
            return JsonResponse({'error': 1, 'msg': '获取动态成功', 'data': []})
        activities_need = []
        for activity in activities:
            user_act = {
                "id": activity.id,
                "type": activity.type,
                "create_time": activity.create_time,
                "programs": activity.programs,
                "t_id": activity.t_id,
            }
            activities_need.append(user_act)
        return JsonResponse({'error': 1, 'msg': '获取动态成功', 'data': activities_need})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def get_admin_spaces(request, uid):
    if request.method == 'GET':
        uid = int(uid)
        try:
            follow = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})
        try:
            studyspaces = StudySpaces.objects.filter(creator_id=uid)
        except:
            return JsonResponse({'error': 1, 'msg': '获取管理空间成功', 'data': []})
        studyspaces_need = []
        for studyspace in studyspaces:
            user_act = {
                "id": studyspace.id,
                "space_name": studyspace.space_name,
                "create_time": studyspace.create_time,
                "space_introduction": studyspace.space_introduction,
                "space_index": studyspace.space_index,
                "space_picture": studyspace.space_picture
            }
            studyspaces_need.append(user_act)
        return JsonResponse({'error': 1, 'msg': '获取管理空间成功', 'data': studyspaces_need})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def get_follow_spaces(request, uid):
    if request.method == 'GET':
        uid = int(uid)
        try:
            follow = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})
        follows = Follows.objects.filter(following=uid, followed_type='spaces')
        studyspaces = []
        for follow in follows:
            studyspaces.append(StudySpaces.objects.get(id=follow.followed_id))
        studyspaces_need = []
        for studyspace in studyspaces:
            user_act = {
                "id": studyspace.id,
                "space_name": studyspace.space_name,
                "create_time": studyspace.create_time,
                "space_introduction": studyspace.space_introduction,
                "space_index": studyspace.space_index,
                "space_picture": studyspace.space_picture
            }
            studyspaces_need.append(user_act)
        return JsonResponse({'error': 1, 'msg': '获取关注空间成功', 'data': studyspaces_need})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def get_resources(request, uid):
    if request.method == 'GET':
        uid = int(uid)
        try:
            follow = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})
        try:
            resources = SpaceResources.objects.filter(user_id=uid)
        except:
            return JsonResponse({'error': 1, 'msg': '获取资源成功', 'data': []})
        resources_need = []

        for resource in resources:
            studyspace = StudySpaces.objects.get(id=resource.space_id)
            user_act = {
                "id": resource.id,
                "space_name": studyspace.space_name,
                "create_time": resource.create_time,
                "file_name": resource.file_name,
                "from_space_id": studyspace.id,
            }
            resources_need.append(user_act)
        return JsonResponse({'error': 1, 'msg': '获取资源成功', 'data': resources_need})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def get_questions(request, uid):
    if request.method == 'GET':
        uid = int(uid)
        try:
            follow = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})
        try:
            questions = SpaceQuestions.objects.filter(user_id=uid)
        except:
            return JsonResponse({'error': 1, 'msg': '获取提问成功', 'data': []})
        questions_need = []

        for question in questions:
            studyspace = StudySpaces.objects.get(id=question.space_id)
            user_act = {
                "id": question.id,
                "space_name": studyspace.space_name,
                "question_title": question.title,
                "create_time": question.create_time,
                "from_space_id": studyspace.id,
                "uid": uid,
            }
            questions_need.append(user_act)
        return JsonResponse({'error': 1, 'msg': '获取提问成功', 'data': questions_need})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def get_answers(request, uid):
    if request.method == 'GET':
        uid = int(uid)
        try:
            follow = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})
        try:
            answers = SpaceComments.objects.filter(user_id=uid, comment_type='answer')
        except:
            return JsonResponse({'error': 1, 'msg': '获取回答成功', 'data': []})
        answers_need = []

        for answer in answers:
            studyspace = StudySpaces.objects.get(id=answer.space_id)
            user_act = {
                "id": answer.id,
                "space_name": studyspace.space_name,
                "content": answer.content,
                "create_time": answer.create_time,
                "from_space_id": studyspace.id,
                "uid": uid,
            }
            answers_need.append(user_act)
        return JsonResponse({'error': 1, 'msg': '获取回答成功', 'data': answers_need})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def get_exercises(request, uid):
    if request.method == 'GET':
        uid = int(uid)
        try:
            follow = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})
        try:
            exercises = SpaceExercises.objects.filter(user_id=uid)
        except:
            return JsonResponse({'error': 1, 'msg': '获取习题成功', 'data': []})
        exercises_need = []

        for exercise in exercises:
            studyspace = StudySpaces.objects.get(id=exercise.space_id)
            user_act = {
                "id": exercise.id,
                "space_name": studyspace.space_name,
                "content": exercise.content,
                "create_time": exercise.create_time,
                "from_space_id": studyspace.space_id,
                "difficulty": exercise.difficulty,
                "type": exercise.type,
                "uid": uid,
            }
            exercises_need.append(user_act)
        return JsonResponse({'error': 1, 'msg': '获取习题成功', 'data': exercises_need})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def get_collects_resources(request, uid):
    if request.method == 'GET':
        uid = int(uid)
        try:
            user_id = request.session['uid']
        except:
            return JsonResponse({'error': 1014, 'msg': "没有登录"})
        try:
            follow = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})
        if uid != user_id:
            return JsonResponse({'error': 1013, 'msg': "这不是你的主页，不能观看哦"})
        try:
            collects = Collects.objects.filter(collect_type='resources', hosts_id=uid)
        except:
            return JsonResponse({'error': 1, 'msg': '获取资源成功', 'data': []})
        resources_need = []

        for collect in collects:
            r_id = collect.collect_id
            resource = SpaceResources.objects.get(id=r_id)
            studyspace = StudySpaces.objects.get(id=resource.space_id)
            user_act = {
                "id": resource.id,
                "space_name": studyspace.space_name,
                "create_time": resource.create_time,
                "file_name": resource.file_name,
                "from_space_id": studyspace.id,
            }
            resources_need.append(user_act)
        return JsonResponse({'error': 1, 'msg': '获取资源成功', 'data': resources_need})

    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def get_collects_questions(request, uid):
    if request.method == 'GET':
        uid = int(uid)
        try:
            user_id = request.session['uid']
        except:
            return JsonResponse({'error': 1014, 'msg': "没有登录"})
        try:
            follow = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})
        if uid != user_id:
            return JsonResponse({'error': 1013, 'msg': "这不是你的主页，不能观看哦"})
        try:
            collects = Collects.objects.filter(collect_type='questions', hosts_id=uid)
        except:
            return JsonResponse({'error': 1, 'msg': '获取提问成功', 'data': []})
        questions_need = []

        for collect in collects:
            q_id = collect.collect_id
            question = SpaceResources.objects.get(id=q_id)
            studyspace = StudySpaces.objects.get(id=question.space_id)
            user_act = {
                "id": question.id,
                "space_name": studyspace.space_name,
                "question_title": question.title,
                "create_time": question.create_time,
                "from_space_id": studyspace.id,
                "uid": uid,
            }
            questions_need.append(user_act)
        return JsonResponse({'error': 1, 'msg': '获取提问成功', 'data': questions_need})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def get_collects_answers(request, uid):
    if request.method == 'GET':
        uid = int(uid)
        try:
            user_id = request.session['uid']
        except:
            return JsonResponse({'error': 1014, 'msg': "没有登录"})
        try:
            follow = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})
        if uid != user_id:
            return JsonResponse({'error': 1013, 'msg': "这不是你的主页，不能观看哦"})
        try:
            collects = Collects.objects.filter(collect_type='answers', hosts_id=uid)
        except:
            return JsonResponse({'error': 1, 'msg': '获取回答成功', 'data': []})
        answers_need = []

        for collect in collects:
            a_id = collect.collect_id
            answer = SpaceResources.objects.filter(id=a_id)
            studyspace = StudySpaces.objects.filter(id=answer.space_id)
            user_act = {
                "id": answer.id,
                "space_name": studyspace.space_name,
                "content": answer.content,
                "create_time": answer.create_time,
                "from_space_id": studyspace.id,
                "uid": uid,
            }
            answers_need.append(user_act)
        return JsonResponse({'error': 1, 'msg': '获取回答成功', 'data': answers_need})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def get_collects_exercises(request, uid):
    if request.method == 'GET':
        uid = int(uid)
        try:
            user_id = request.session['uid']
        except:
            return JsonResponse({'error': 1014, 'msg': "没有登录"})
        try:
            follow = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})
        if uid != user_id:
            return JsonResponse({'error': 1013, 'msg': "这不是你的主页，不能观看哦"})
        try:
            collects = Collects.objects.filter(collect_type='exercises', hosts_id=uid)
        except:
            return JsonResponse({'error': 1, 'msg': '获取习题成功', 'data': []})
        exercises_need = []

        for collect in collects:
            e_id = collect.collect_id
            exercise = SpaceResources.objects.get(id=e_id)
            studyspace = StudySpaces.objects.get(id=exercise.space_id)
            user_act = {
                "id": exercise.id,
                "space_name": studyspace.space_name,
                "content": exercise.content,
                "create_time": exercise.create_time,
                "from_space_id": studyspace.space_id,
                "difficulty": exercise.difficulty,
                "type": exercise.type,
                "uid": uid,
            }
            exercises_need.append(user_act)
        return JsonResponse({'error': 1, 'msg': '获取习题成功', 'data': exercises_need})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def get_followings(request, uid):
    if request.method == 'GET':
        uid = int(uid)
        try:
            follow = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})
        user_need = []
        try:
            follows = Follows.objects.filter(following=uid, followed_type='people')
        except:
            return JsonResponse({'error': 1, 'msg': '获取关注列表成功', 'data': user_need})

        for follow in follows:
            user = User.objects.get(id=follow.followed_id)
            user_act = {
                "uid": user.id,
                "username": user.username,
            }
            user_need.append(user_act)

        return JsonResponse({'error': 1, 'msg': '获取关注列表成功', 'data': user_need})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def get_fans(request, uid):
    if request.method == 'GET':
        uid = int(uid)
        try:
            follow = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})
        try:
            follows = Follows.objects.filter(followed_id=uid, followed_type='people')
        except:
            return JsonResponse({'error': 1, 'msg': '获取粉丝列表成功', 'data': []})
        fan_need = []

        for follow in follows:
            user = User.objects.get(id=follow.following)
            user_act = {
                "uid": user.id,
                "username": user.username,
                "fans": user.followers,
            }
            fan_need.append(user_act)
        return JsonResponse({'error': 1, 'msg': '获取粉丝列表成功', 'data': fan_need})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def follow_people(request, uid):
    if request.method == 'POST':
        try:
            user_id = request.session['uid']
        except:
            return JsonResponse({'error': 1014, 'msg': "没有登录"})
        uid = int(uid)

        try:
            follow = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})

        if uid == user_id:
            return JsonResponse({'error': 1013, 'msg': "不能关注自己哦"})

        fan = User.objects.get(id=user_id)

        try:
            Follows.objects.get(following=uid, followed_id=user_id)
        except:
            fan.followings += 1
            follow.followers += 1

            new_follow = Follows()
            new_follow.followed_type = 'people'
            new_follow.followed_id = user_id
            new_follow.following = follow
            new_follow.save()

            return JsonResponse({'error': 1, 'msg': '关注成功'})

        fan.followings -= 1
        follow.followers -= 1
        follow.delete()
        follow.id = uid
        follow.save()
        return JsonResponse({'error': 1, 'msg': '取消关注成功'})

    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})

import os

from django.forms import model_to_dict
import app01.models as data
import time

import datetime
import json
import re

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from pytz import utc

from app01.models import *
from tools.emails import *
from django.db.models import Q


# Create your views here.


def get_time_now():
    create_time = time.localtime(time.time())
    create_time = str(create_time.tm_year) + "-" + str(create_time.tm_mon) + "-" + \
                  str(create_time.tm_mday) + " " + str(create_time.tm_hour) + ":" + \
                  str(create_time.tm_min) + ":" + str(create_time.tm_sec)
    return create_time


def exist_check(*args):
    for each in args:
        if each is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少'
            })
    return None


def order_query_list(query_list, method):
    if method == '最多点赞':
        query_list.sort(key=lambda k: (k.get('likes', 0)), reverse=True)
    elif method == '最多关注':
        query_list.sort(key=lambda k: (k.get('follows', 0)), reverse=True)
    elif method == '最多讨论':
        query_list.sort(key=lambda k: (k.get('comments', 0)), reverse=True)
    return query_list


# 3是创建者，2是管理员，1是可访问普通用户，0是不可访问
def space_permissions_check(ses, space):
    if space.creator_id.id == ses.get('user_id'):
        return 3
    perm = space.space_permission
    member = data.SpaceMembers.objects.filter(space_id=space, user_id=ses.get('user_id'))
    if member.count() == 0 and perm != 0:
        return 0
    elif member.count() == 0 and perm == 0:
        return 1
    elif member[0].is_admin == 0:
        return 1
    elif member[0].is_admin != 0:
        return 2
    else:
        return -1


# 1资源，2讨论，3习题，4群组，5评论自身（可以不要）
def get_comments_list(space, ele_id, ele_type):
    if ele_type == '资源':
        type_id = 1
    elif ele_type == '讨论':
        type_id = 2
    elif ele_type == '习题':
        type_id = 3
    elif ele_type == '群组':
        type_id = 4
    comments_set = data.SpaceComments.objects.filter(space_id=space, element_id=ele_id, comment_type=type_id)
    c_list = []
    for each in comments_set:
        each_dict = model_to_dict(each, exclude=['create_time'])
        each_dict['create_time'] = each.create_time
        each_dict['likes'] = data.Likes.objects.filter(liked_id=ele_id, liked_type=ele_type).count()
        each_dict['follows'] = data.Follows.objects.filter(followed_id=ele_id, followed_type=ele_type).count()
        c_list.append(each_dict)
    return c_list


# 1资源，2讨论，3习题，4群组，5评论自身（可以不要）
def make_comment(space, content, ele_id, ele_type, user_id):
    if ele_type == '资源':
        data.SpaceComments.objects.create(space_id=space,
                                          user_id=get_user_by_id(user_id),
                                          element_id=ele_id,
                                          comment_type=1,
                                          content=content,
                                          create_time=get_time_now()
                                          )
    elif ele_type == '讨论':
        data.SpaceComments.objects.create(space_id=space,
                                          user_id=get_user_by_id(user_id),
                                          element_id=ele_id,
                                          comment_type=2,
                                          content=content,
                                          create_time=get_time_now()
                                          )
    elif ele_type == '习题':
        data.SpaceComments.objects.create(space_id=space,
                                          user_id=get_user_by_id(user_id),
                                          element_id=ele_id,
                                          comment_type=3,
                                          content=content,
                                          create_time=get_time_now()
                                          )
    elif ele_type == '群组':
        data.SpaceComments.objects.create(space_id=space,
                                          user_id=get_user_by_id(user_id),
                                          element_id=ele_id,
                                          comment_type=4,
                                          content=content,
                                          create_time=get_time_now()
                                          )


def get_user_by_id(uid):
    return data.User.objects.get(id=uid)


def init_ret_dict(ses, space):
    admin_set = data.SpaceMembers.objects.filter(space_id=space, is_admin=1)
    member_set = data.SpaceMembers.objects.filter(space_id=space, is_admin=0)
    creator = data.User.objects.filter(id=space.creator_id.id)[0]
    member_list = []
    admin_list = [model_to_dict(creator)]
    for each in admin_set:
        each_dict = model_to_dict(each)
        admin_list.append(each_dict)
    for each in member_set:
        each_dict = model_to_dict(each)
        member_list.append(each_dict)
    ret_dict = {'space_name': space.space_name, 'space_index': space.space_index,
                'space_introduction': space.space_introduction,
                # 'space_picture': space.space_picture,
                'space_permission': space.space_permission,
                'create_time': space.create_time,
                'likes_num': data.SpaceLikes.objects.filter(space_id=space).count(),
                'follows_num': data.SpaceFollows.objects.filter(space_id=space).count(),
                'resources_num': data.SpaceResources.objects.filter(space_id=space).count(),
                'exercises_num': data.SpaceExercises.objects.filter(space_id=space).count(),
                'questions_num': data.SpaceQuestions.objects.filter(space_id=space).count(),
                'groups_num': data.SpaceGroups.objects.filter(space_id=space).count(),
                'notices_num': data.SpaceNotices.objects.filter(space_id=space).count(),
                'admin_list': admin_list,
                'member_list': member_list,
                'user_permission': space_permissions_check(ses, space),
                'liked': False,
                'followed': False,
                }
    return ret_dict


def like_follow_space(space, ses, is_like, is_follow, ret_dict, query_list, total, page):
    if is_like:
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'})
        if ret_dict['liked']:
            data.SpaceLikes.objects.filter(space_id=space, user_id=get_user_by_id(ses['user_id'])).delete()
            ret_dict['liked'] = False
        else:
            activities_add(ses['user_id'], 0, '学习空间', space.id, 0, '点赞了学习空间')
            data.SpaceLikes.objects.create(space_id=space,
                                           user_id=get_user_by_id(ses['user_id']), like_time=get_time_now())
            ret_dict['liked'] = True
        return JsonResponse({
            'errno': '200',
            'msg': '点赞/取消点赞成功',
            'data': ret_dict,
            'list': query_list[page * 10 - 10:page * 10 - 1],
            'total': total
        })

    elif is_follow:
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'})
        if ret_dict['followed']:
            data.SpaceFollows.objects.filter(space_id=space, user_id=get_user_by_id(ses['user_id'])).delete()
            ret_dict['followed'] = False
        else:
            activities_add(ses['user_id'], 0, '学习空间', space.id, 0, '关注了学习空间')
            data.SpaceFollows.objects.create(space_id=space,
                                             user_id=get_user_by_id(ses['user_id']), follow_time=get_time_now())
            ret_dict['followed'] = True
        return JsonResponse({
            'errno': '200',
            'msg': '收藏/取消收藏成功',
            'data': ret_dict,
            'list': query_list[page * 10 - 10:page * 10 - 1],
            'total': total
        })
    else:
        return JsonResponse({
            'errno': '200',
            'msg': '查询成功',
            'data': ret_dict,
            'list': query_list[page * 10 - 10:page * 10 - 1],
            'total': total
        })


def like_follow_element(space, ses, is_like, is_follow, is_like_element, is_follow_element,
                        ret_dict, ele_type, ele_dict, comments_list):
    if is_like:
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'})
        if ret_dict['liked']:
            data.SpaceLikes.objects.filter(space_id=space, user_id=get_user_by_id(ses['user_id'])).delete()
            ret_dict['liked'] = False
        else:
            activities_add(ses['user_id'], 0, ele_type, space.id, 0, '点赞了'+ele_type)
            data.SpaceLikes.objects.create(space_id=space,
                                           user_id=get_user_by_id(ses['user_id']), like_time=get_time_now())
            ret_dict['liked'] = True
        return JsonResponse({
            'errno': '200',
            'msg': '点赞/取消点赞成功',
            'data': ret_dict,
            'element': ele_dict,
            'comments_list': comments_list
        })

    elif is_follow:
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'})
        if ret_dict['followed']:
            data.SpaceFollows.objects.filter(space_id=space, user_id=get_user_by_id(ses['user_id'])).delete()
            ret_dict['followed'] = False
        else:
            activities_add(ses['user_id'], 0, ele_type, space.id, 0, '关注了' + ele_type)
            data.SpaceFollows.objects.create(space_id=space,
                                             user_id=get_user_by_id(ses['user_id']), follow_time=get_time_now())
            ret_dict['followed'] = True
        return JsonResponse({
            'errno': '200',
            'msg': '收藏/取消收藏成功',
            'data': ret_dict,
            'element': ele_dict,
            'comments_list': comments_list
        })

    elif is_like_element:
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'})
        if ele_dict['ele_liked']:
            data.Likes.objects.filter(hosts=get_user_by_id(ses['user_id']),
                                      liked_type=ele_type, liked_id=ele_dict['id']).delete()
            ele_dict['ele_liked'] = False
        else:
            activities_add(ses['user_id'], 0, ele_type, ele_dict['id'], space.id, '点赞了' + ele_type)
            data.Likes.objects.create(hosts=get_user_by_id(ses['user_id']),
                                      liked_type=ele_type, liked_id=ele_dict['id'], liked_time=get_time_now())
            ele_dict['ele_liked'] = True
        return JsonResponse({
            'errno': '200',
            'msg': '点赞/取消点赞元素成功',
            'data': ret_dict,
            'element': ele_dict,
            'comments_list': comments_list
        })

    elif is_follow_element:
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'})
        if ele_dict['ele_followed']:
            data.Follows.objects.filter(following=get_user_by_id(ses['user_id']),
                                        followed_type=ele_type, followed_id=ele_dict['id']).delete()
            ele_dict['ele_followed'] = False
        else:
            activities_add(ses['user_id'], 0, ele_type, ele_dict['id'], space.id, '关注了' + ele_type)
            data.Follows.objects.create(following=get_user_by_id(ses['user_id']), followed_type=ele_type,
                                        followed_id=ele_dict['id'], followed_time=get_time_now())
            ele_dict['ele_followed'] = True
        return JsonResponse({
            'errno': '200',
            'msg': '收藏/取消收藏元素成功',
            'data': ret_dict,
            'element': ele_dict,
            'comments_list': comments_list
        })

    else:
        return JsonResponse({
            'errno': '200',
            'msg': '查询成功',
            'data': ret_dict,
            'element': ele_dict,
            'comments_list': comments_list
        })


'''
需要传递的数据:
show:筛选学习空间的条件(string,例如:全部空间、最近访问、关注空间、管理空间等等)
order:学习空间排序方式(string,例如:最多点赞、最多关注、最近更新、最早更新、最近创建、最早创建),如果筛选条件为最近访问则该条件可以为空
page:需要显示第几页(int)

返回内容：
data：符合筛选条件的当前页码的学习空间列表，顺序按照排序方式排序，每个元素均为一个字典，其中内容见数据库
total：符合筛选条件的所有学习空间数量
'''


@csrf_exempt
def spaces_index(request):
    ses = request.session
    if request.method == 'POST':
        recv = request.POST
        method = request.POST.get('sort')
        if method is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少sort'})
        elif method == '最多点赞':
            order = 'id'
        elif method == '最多关注':
            order = 'id'
        elif method == '最近更新':
            order = '-last_update_time'
        elif method == '最早更新':
            order = 'last_update_time'
        elif method == '最近创建':
            order = '-create_time'
        elif method == '最早创建':
            order = 'create_time'
        else:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数order不合法'})
        # 查询条件
        page = request.POST.get('page')
        if page is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少page'})
        page = int(page)

        query_list = []
        if recv.get('show') == '全部空间':
            query_set = data.StudySpaces.objects.all().order_by(order)
            for each in query_set:
                each_dict = model_to_dict(each, exclude=['space_picture'])
                each_dict['likes'] = data.SpaceLikes.objects.filter(space_id=each_dict['id']).count()
                each_dict['follows'] = data.SpaceFollows.objects.filter(space_id=each_dict['id']).count()
                query_list.append(each_dict)
            total = len(query_list)
            query_list = order_query_list(query_list, method)
            print(query_list[0])
            return JsonResponse({
                'errno': '200',
                'msg': '查询全部空间成功',
                'data': query_list[page * 10 - 10:page * 10 - 1],
                'total': total,
            })

        elif recv.get('show') == '最近访问':
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})
            id_list = data.SpaceLooks.objects.filter(user_id=get_user_by_id(ses['user_id'])).values('space_id')
            space_list = data.StudySpaces.objects.all.order_by('-SpaceLooks__watch_time')
            for each in space_list:
                if each.id == id_list.space_id:
                    each_dict = model_to_dict(each)
                    each_dict['likes'] = data.SpaceLikes.objects.filter(space_id=each_dict['id']).count()
                    each_dict['follows'] = data.SpaceFollows.objects.filter(space_id=each_dict['id']).count()
                    query_list.append(each_dict)
            total = len(query_list)
            query_list = order_query_list(query_list, method)
            return JsonResponse({
                'errno': '201',
                'msg': '查询最近访问成功',
                'data': query_list[page * 10 - 10:page * 10 - 1],
                'total': total,
            })

        elif recv.get('show') == '关注空间':
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})
            id_set = data.Follows.objects.filter(user_id=get_user_by_id(ses['user_id'])).values('space_id')
            space_set = data.StudySpaces.objects.all.order_by(order)
            for each in space_set:
                if each.id == id_set.space_id:
                    each_dict = model_to_dict(each)
                    each_dict['likes'] = data.SpaceLikes.objects.filter(space_id=each_dict['id']).count()
                    each_dict['follows'] = data.SpaceFollows.objects.filter(space_id=each_dict['id']).count()
                    query_list.append(each_dict)
            total = len(query_list)
            query_list = order_query_list(query_list, method)
            return JsonResponse({
                'errno': '202',
                'msg': '查询关注空间成功',
                'data': query_list[page * 10 - 10:page * 10 - 1],
                'total': total,
            })

        elif recv.get('show') == '管理空间':
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})
            space_set = data.StudySpaces.objects.filter(user_id=get_user_by_id(ses['user_id'])).order_by(order)
            for each in space_set:
                each_dict = model_to_dict(each)
                each_dict['likes'] = data.SpaceLikes.objects.filter(space_id=each_dict['id']).count()
                each_dict['follows'] = data.SpaceFollows.objects.filter(space_id=each_dict['id']).count()
                query_list.append(each_dict)
            total = len(query_list)
            query_list = order_query_list(query_list, method)
            return JsonResponse({
                'errno': '203',
                'msg': '查询管理空间成功',
                'data': query_list[page * 10 - 10:page * 10 - 1],
                'total': total,
            })

        else:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少show或者不合法'})
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


'''
需要传递的数据:
is_create: int 代表是否点击了最终确认创建按钮
space_name: string 新空间名
space_introduction: string 新空间介绍
space_permission: int 新空间访问权限，0为公有，非0为私有
space_picture: 图片文件 新空间封面，为空则表示未上传，扩展名暂时只能是jpg，png
'''


@csrf_exempt
def space_create(request):
    ses = request.session

    if request.method == 'POST':
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'})
        user_now = User.objects.get(id=int(ses.get('user_id')))
        is_create = request.POST.get('is_create')
        if is_create is None:
            return JsonResponse({
                'errno': '200',
                'msg': '等待提交'
            })
        space_name = request.POST.get('space_name')
        if space_name is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少space_name'})
        space_introduction = request.POST.get('space_introduction')
        if space_introduction is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少space_introduction'})
        space_permission = request.POST.get('space_permission')
        if space_permission is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少space_permission'})
        space_picture = request.FILES.get('space_picture')
        create_time = get_time_now()
        if space_picture is None:
            new_space = data.StudySpaces(space_name=space_name,
                                         space_introduction=space_introduction,
                                         space_permission=space_permission,
                                         create_time=create_time,
                                         last_update_time=create_time,
                                         creator_id=user_now)
        else:
            extended_name = os.path.splitext(space_picture.name)[-1]
            allowed_name = ['.jpg', '.png']
            if extended_name not in allowed_name:
                return JsonResponse({
                    'errno': '402',
                    'msg': '上传图片后缀名不合法'})
            new_space = data.StudySpaces(space_name=space_name,
                                         space_introduction=space_introduction,
                                         space_permission=space_permission,
                                         create_time=create_time,
                                         last_update_time=create_time,
                                         space_picture=space_picture,
                                         creator_id=user_now)
        try:
            new_space.save()
        except RuntimeError:
            return JsonResponse({
                'errno': '403',
                'msg': '数据库操作失败'})
        activities_add(ses['user_id'], 0, "学习空间", new_space.id, 0, '创建了学习空间')
        return JsonResponse({
            'errno': '200',
            'msg': '创建学习空间成功'})
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


'''
需要传递的参数
is_edit: int 代表此次请求是否是申请编辑主页内容，True/1代表是
is_like: int 代表是否点击了点赞按钮，True/1代表是
is_follow: int 代表是否点击了收藏按钮，True/1代表是
（以上三个至多有一个为True）
new_index: string 如果是编辑主页，则还需要这个参数代表修改后的内容

返回内容
data：ret_dict，包含学习空间需要显示信息的字典


'''


@csrf_exempt
def space_main(request, space_id):
    if request.method == 'POST':
        ses = request.session
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})
        ret_dict = init_ret_dict(ses, space)
        is_edit = request.POST.get('is_edit')
        is_like = request.POST.get('is_like')
        is_follow = request.POST.get('is_follow')
        if ses.get('user_id') is not None:
            liked = data.SpaceLikes.objects.filter(space_id=space, user_id=get_user_by_id(ses['user_id'])).count()
            if liked == 1:
                ret_dict['liked'] = True
            followed = data.SpaceFollows.objects.filter(space_id=space, user_id=get_user_by_id(ses['user_id'])).count()
            if followed == 1:
                ret_dict['followed'] = True

        if is_edit:
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})
            new_index = request.POST.get('new_content')
            space.space_index = new_index
            try:
                space.save()
            except RuntimeError:
                return JsonResponse({
                    'errno': '403',
                    'msg': '数据库操作失败'})
            return JsonResponse({
                'errno': '200',
                'msg': '修改主页成功',
                'data': ret_dict,
            })
        elif is_like:
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})
            if ret_dict['liked']:
                data.SpaceLikes.objects.filter(space_id=space, user_id=get_user_by_id(ses['user_id'])).delete()
                ret_dict['liked'] = False
            else:
                data.SpaceLikes.objects.create(space_id=space, user_id=get_user_by_id(ses['user_id']),
                                               like_time=get_time_now())
                ret_dict['liked'] = True
            return JsonResponse({
                'errno': '200',
                'msg': '点赞/取消点赞成功',
                'data': ret_dict,
            })
        elif is_follow:
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})
            if ret_dict['followed']:
                data.SpaceFollows.objects.filter(space_id=space, user_id=get_user_by_id(ses['user_id'])).delete()
                ret_dict['followed'] = False
            else:
                data.SpaceFollows.objects.create(space_id=space, user_id=get_user_by_id(ses['user_id']),
                                                 like_time=get_time_now())
                ret_dict['followed'] = True
            return JsonResponse({
                'errno': '200',
                'msg': '收藏/取消收藏成功',
                'data': ret_dict,
            })
        else:
            return JsonResponse({
                'errno': '200',
                'msg': '查询成功',
                'data': ret_dict,
            })

    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


'''
需要的参数：
page: int 当前页数
order: string 排序方式：最多点赞、最近更新、最早更新、资源标题（按字典序排序）
is_like: int 代表是否点击了点赞按钮，True/1代表是（这个为True只是代表点击了点赞按钮，也可以是取消点赞的意思）
is_follow: int 代表是否点击了收藏按钮，True/1代表是

返回内容
data：ret_dict
list：当前页码的资源列表（10个）
total：该学习空间资源总数

'''


@csrf_exempt
def space_resources_index(request, space_id):
    if request.method == 'POST':
        ses = request.session
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})
        ret_dict = init_ret_dict(ses, space)
        page = request.POST.get('page')
        if page is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'GET参数缺少page'})
        page = int(page)

        query_list = []
        method = request.POST.get('sort')
        if method is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'GET参数缺少sort'})
        elif method == '最多点赞':
            order = '-id'
        elif method == '资源标题':
            order = 'resource_name'
        elif method == '最近更新':
            order = '-last_update_time'
        elif method == '最早更新':
            order = 'last_update_time'
        else:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数order不合法'})
        resources_set = data.SpaceResources.objects.filter(space_id=space).order_by(order)
        total = resources_set.count()
        for each in resources_set:
            each_dict = model_to_dict(each, exclude=['file'])
            each_dict['likes'] = data.Likes.objects.filter(liked_type='资源', liked_id=each_dict['id']).count()
            each_dict['follows'] = data.Follows.objects.filter(followed_type='资源',
                                                               followed_id=each_dict['id']).count()
            query_list.append(each_dict)
        query_list = order_query_list(query_list, method)

        is_like = request.POST.get('is_like')
        is_follow = request.POST.get('is_follow')

        if ses.get('user_id') is not None:
            liked = data.SpaceLikes.objects.filter(space_id=space, user_id=get_user_by_id(ses['user_id'])).count()
            if liked == 1:
                ret_dict['liked'] = True
            followed = data.SpaceFollows.objects.filter(space_id=space, user_id=get_user_by_id(ses['user_id'])).count()
            if followed == 1:
                ret_dict['followed'] = True

        return like_follow_space(space, ses, is_like, is_follow, ret_dict, query_list, total, page)

    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


'''
需要传递的数据:
page: int 当前页数
is_like: int 代表是否点击了点赞按钮，True/1代表是
is_follow: int 代表是否点击了收藏按钮，True/1代表是
（以上两个至多一个True，学习空间任何位置都能点击点赞收藏按钮，因此每个路由都有这两个参数）
*群组没有排序
'''


@csrf_exempt
def space_groups_index(request, space_id):
    if request.method == 'POST':
        ses = request.session
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})
        ret_dict = init_ret_dict(ses, space)
        page = request.POST.get('page')
        if page is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少page'})
        page = int(page)

        query_list = []
        groups_set = data.SpaceGroups.objects.filter(space_id=space)
        total = groups_set.count()
        for each in groups_set:
            each_dict = model_to_dict(each)
            each_dict['member_num'] = each.members.count()
            query_list.append(each_dict)
        if ses.get('user_id') is not None:
            liked = data.SpaceLikes.objects.filter(space_id=space, user_id=get_user_by_id(ses['user_id'])).count()
            if liked == 1:
                ret_dict['liked'] = True
            followed = data.SpaceFollows.objects.filter(space_id=space, user_id=get_user_by_id(ses['user_id'])).count()
            if followed == 1:
                ret_dict['followed'] = True
        is_like = request.POST.get('is_like')
        is_follow = request.POST.get('is_follow')

        return like_follow_space(space, ses, is_like, is_follow, ret_dict, query_list, total, page)

    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


'''

'''


@csrf_exempt
def space_questions_index(request, space_id):
    if request.method == 'POST':
        ses = request.session
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})
        ret_dict = init_ret_dict(ses, space)
        page = request.POST.get('page')
        if page is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少page'})
        page = int(page)

        method = request.POST.get('sort')
        if method is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少order'})
        elif method == '最多点赞':
            order = 'id'
        elif method == '最多讨论':
            order = 'id'
        elif method == '最近更新':
            order = '-last_update_time'
        elif method == '最新创建':
            order = '-create_time'
        else:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数order不合法'})

        query_list = []
        questions_set = data.SpaceQuestions.objects.filter(space_id=space).order_by(order)
        total = questions_set.count()
        for each in questions_set:
            each_dict = model_to_dict(each)
            each_dict['likes'] = data.Likes.objects.filter(liked_type='讨论', liked_id=each_dict['id']).count()
            each_dict['comments'] = len(get_comments_list(space, each_dict['id'], '讨论'))
            each_dict['follows'] = data.Follows.objects.filter(liked_type='讨论', liked_id=each_dict['id']).count()
            query_list.append(each_dict)
        query_list = order_query_list(query_list, method)

        is_like = request.POST.get('is_like')
        is_follow = request.POST.get('is_follow')
        return like_follow_space(space, ses, is_like, is_follow, ret_dict, query_list, total, page)

    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


'''
习题没有排序
'''


@csrf_exempt
def space_exercises_index(request, space_id):
    if request.method == 'POST':
        ses = request.session
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})
        ret_dict = init_ret_dict(ses, space)
        page = request.POST.get('page')
        if page is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少page'})
        page = int(page)

        query_list = []
        exercises_set = data.SpaceExercises.objects.filter(space_id=space)
        total = exercises_set.count()
        for each in exercises_set:
            each_dict = model_to_dict(each)
            each_dict['likes'] = data.Likes.objects.filter(liked_type='习题', liked_id=each_dict['id']).count()
            each_dict['comments'] = len(get_comments_list(space, each_dict['id'], '习题'))
            each_dict['follows'] = data.Follows.objects.filter(liked_type='习题', liked_id=each_dict['id']).count()
            query_list.append(each_dict)

        is_like = request.POST.get('is_like')
        is_follow = request.POST.get('is_follow')
        return like_follow_space(space, ses, is_like, is_follow, ret_dict, query_list, total, page)

    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


@csrf_exempt
def space_notices_index(request, space_id):
    if request.method == 'POST':
        ses = request.session
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})
        ret_dict = init_ret_dict(ses, space)
        page = request.POST.get('page')
        if page is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少page'})
        page = int(page)

        query_list = []
        notices_set = data.SpaceNotices.objects.filter(space_id=space).order_by('-last_update_time')
        total = notices_set.count()
        return JsonResponse({
            'errno': '200',
            'msg': '查询成功',
            'data': ret_dict,
            'list': query_list[page * 10 - 10:page * 10 - 1],
            'total': total
        })

    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


'''
需要的参数：
is_like: int 代表是否点击了点赞按钮，True/1代表是
is_follow: int 代表是否点击了收藏按钮，True/1代表是
is_delete: int 代表是否申请删除自己创建的资源内容，True/1代表是
is_like_element: int 代表是否是点击了点赞资源按钮，True/1代表是
is_follow_element: int 代表是否是点击了收藏资源按钮，True/1代表是
is_comment: int 1/0
（以上五个至多一个True，学习空间除了创建界面任何位置都能点击点赞收藏按钮）
content: string 评论内容

返回内容
data：ret_dict
element：该资源的字典
comments_list：该资源的评论字典列表，新加key：commenter 评论者的用户字典（还没写，如果觉得麻烦我就拿出来，字典里面的字典确实难访问）
'''


@csrf_exempt
def space_resources(request, space_id, resources_id):
    if request.method == 'POST':
        ses = request.session
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})
        resource = data.SpaceResources.objects.filter(id=resources_id)
        if resource.count() != 1:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到资源'})
        ret_dict = init_ret_dict(ses, space)
        is_delete = request.POST.get('is_delete')
        is_comment = request.POST.get('is_comment')
        resource = resource[0]
        ele_type = '资源'
        if is_delete:
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})
            resource = data.SpaceResources.objects.filter(id=resources_id)

            if resource.user_id != ses.get('user_id'):
                return JsonResponse({
                    'errno': '407',
                    'msg': '待删除资源不是当前用户所创建'})
            resource.delete()
            return JsonResponse({
                'errno': '200',
                'msg': '删除成功'})
        elif is_comment:
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})
            content = request.POST.get('content')
            ret = exist_check(content)
            if ret is not None:
                return ret
            make_comment(space, content, resources_id, ele_type, ses['user_id'])
            return JsonResponse({
                'errno': '400',
                'msg': '评论成功',
            })

        ele_dict = model_to_dict(resource, exclude=['file'])
        ele_dict['likes'] = data.Likes.objects.filter(liked_type=ele_type, liked_id=ele_dict['id']).count()
        ele_dict['follows'] = data.Follows.objects.filter(followed_type=ele_type, followed_id=ele_dict['id']).count()
        ele_dict['ele_liked'] = False
        ele_dict['ele_followed'] = False
        if ses.get('user_id'):
            if data.Likes.objects.filter(hosts=get_user_by_id(ses['user_id']),
                                         liked_type=ele_type, liked_id=ele_dict['id']).count() == 1:
                ele_dict['ele_liked'] = True
            if data.Follows.objects.filter(following=get_user_by_id(ses['user_id']),
                                           followed_type=ele_type, followed_id=ele_dict['id']).count() == 1:
                ele_dict['ele_followed'] = True

        comments_list = get_comments_list(space, ele_dict['id'], ele_type)
        for each in comments_list:
            commenter = data.User.objects.filter(id=each['user_id'])
            if commenter.count() != 1:
                return JsonResponse({
                    'errno': '402',
                    'msg': '评论者id不存在'})
            each['commenter'] = model_to_dict(commenter[0])

        is_like = request.POST.get('is_like')
        is_follow = request.POST.get('is_follow')
        is_like_element = request.POST.get('is_like_element')
        is_follow_element = request.POST.get('is_follow_element')
        return like_follow_element(space, ses, is_like, is_follow, is_like_element, is_follow_element,
                                   ret_dict, ele_type, ele_dict, comments_list)
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


'''
需要的参数：
is_like: int 代表是否点击了点赞按钮，True/1代表是
is_follow: int 代表是否点击了收藏按钮，True/1代表是
is_delete: int 代表是否申请删除自己创建的资源内容，True/1代表是
is_like_element: int 代表是否是点击了点赞资源按钮，True/1代表是
is_follow_element: int 代表是否是点击了收藏资源按钮，True/1代表是
（以上五个至多一个True，学习空间除了创建界面任何位置都能点击点赞收藏按钮）


返回内容
data：ret_dict
element：该资源的字典
comments_list：该资源的评论字典列表，新加key：commenter 评论者的用户字典（还没写，如果觉得麻烦我就拿出来，字典里面的字典确实难访问）
'''


@csrf_exempt
def space_questions(request, space_id, questions_id):
    if request.method == 'POST':
        ses = request.session
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})
        question = data.SpaceQuestions.objects.filter(id=questions_id)
        if question.count() != 1:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到待删除资源'})
        question = question[0]
        ret_dict = init_ret_dict(ses, space)

        is_delete = request.POST.get('is_delete')
        is_comment = request.POST.get('is_comment')
        ele_type = '讨论'
        if is_delete:
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})

            if question.user_id != ses.get('user_id'):
                return JsonResponse({
                    'errno': '407',
                    'msg': '待删除讨论不是当前用户所创建'})
            question.delete()
            return JsonResponse({
                'errno': '200',
                'msg': '删除成功'})

        elif is_comment:
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})
            content = request.POST.get('content')
            ret = exist_check(content)
            if ret is not None:
                return ret
            make_comment(space, content, questions_id, ele_type, ses['user_id'])
            return JsonResponse({
                'errno': '400',
                'msg': '评论成功'
            })
        ele_dict = model_to_dict(question)
        ele_dict['likes'] = data.Likes.objects.filter(liked_type=ele_type, liked_id=ele_dict['id']).count()
        ele_dict['follows'] = data.Follows.objects.filter(liked_type=ele_type, liked_id=ele_dict['id']).count()

        ele_dict['ele_liked'] = False
        ele_dict['ele_followed'] = False
        if ses.get('user_id'):
            if data.Likes.objects.filter(hosts=get_user_by_id(ses['user_id']),
                                         liked_type=ele_type, liked_id=ele_dict['id']).count() == 1:
                ele_dict['ele_liked'] = True
            if data.Follows.objects.filter(following=get_user_by_id(ses['user_id']),
                                           followed_type=ele_type, followed_id=ele_dict['id']).count() == 1:
                ele_dict['ele_followed'] = True

        comments_list = get_comments_list(space, ele_dict['id'], ele_type)
        for each in comments_list:
            commenter = data.User.objects.filter(id=each['user_id'])
            if commenter.count() != 1:
                return JsonResponse({
                    'errno': '402',
                    'msg': '评论者id不存在'})
            each['commenter'] = model_to_dict(commenter)

        is_like = request.POST.get('is_like')
        is_follow = request.POST.get('is_follow')
        is_like_element = request.POST.get('is_like_element')
        is_follow_element = request.POST.get('is_follow_element')
        return like_follow_element(space, ses, is_like, is_follow, is_like_element, is_follow_element,
                                   ret_dict, ele_type, ele_dict, comments_list)

    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


@csrf_exempt
def space_exercises(request, space_id, exercises_id):
    if request.method == 'POST':
        ses = request.session
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})
        exercise = data.SpaceExercises.objects.filter(id=exercises_id)
        if exercise.count() != 1:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到待删除资源'})
        exercise = exercise[0]
        ret_dict = init_ret_dict(ses, space)

        is_delete = request.POST.get('is_delete')
        is_comment = request.POST.get('is_comment')
        ele_type = '习题'
        if is_delete:
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})

            if exercise.user_id != ses.get('user_id'):
                return JsonResponse({
                    'errno': '407',
                    'msg': '待删除习题不是当前用户所创建'})
            exercise.delete()
            return JsonResponse({
                'errno': '200',
                'msg': '删除成功'})

        elif is_comment:
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})
            content = request.POST.get('content')
            ret = exist_check(content)
            if ret is not None:
                return ret
            make_comment(space, content, exercises_id, ele_type, ses['user_id'])
            return JsonResponse({
                'errno': '400',
                'msg': '评论成功',
            })

        ele_dict = model_to_dict(exercise)
        ele_dict['likes'] = data.Likes.objects.filter(liked_type=ele_type, liked_id=ele_dict['id']).count()
        ele_dict['follows'] = data.Follows.objects.filter(liked_type=ele_type, liked_id=ele_dict['id']).count()

        ele_dict['ele_liked'] = False
        ele_dict['ele_followed'] = False
        if ses.get('user_id'):
            if data.Likes.objects.filter(hosts=get_user_by_id(ses['user_id']),
                                         liked_type=ele_type, liked_id=ele_dict['id']).count() == 1:
                ele_dict['ele_liked'] = True
            if data.Follows.objects.filter(following=get_user_by_id(ses['user_id']),
                                           followed_type=ele_type, followed_id=ele_dict['id']).count() == 1:
                ele_dict['ele_followed'] = True

        comments_list = get_comments_list(space, ele_dict['id'], ele_type)
        for each in comments_list:
            commenter = data.User.objects.filter(id=each['user_id'])
            if commenter.count() != 1:
                return JsonResponse({
                    'errno': '402',
                    'msg': '评论者id不存在'})
            each['commenter'] = model_to_dict(commenter)

        is_like = request.POST.get('is_like')
        is_follow = request.POST.get('is_follow')
        is_like_element = request.POST.get('is_like_element')
        is_follow_element = request.POST.get('is_follow_element')
        return like_follow_element(space, ses, is_like, is_follow, is_like_element, is_follow_element,
                                   ret_dict, ele_type, ele_dict, comments_list)
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


@csrf_exempt
def space_groups(request, space_id, groups_id):
    if request.method == 'POST':
        ses = request.session
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})
        group = data.SpaceGroups.objects.filter(id=groups_id)
        if group.count() != 1:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到待删除资源'})
        group = group[0]
        ret_dict = init_ret_dict(ses, space)

        is_delete = request.POST.get('is_delete')
        if is_delete:
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})

            if group.user_id != ses.get('user_id'):
                return JsonResponse({
                    'errno': '407',
                    'msg': '待删除习题不是当前用户所创建'})
            group.delete()
            return JsonResponse({
                'errno': '200',
                'msg': '删除成功'})

        ele_type = '习题'
        ele_dict = model_to_dict(group)
        ele_dict['likes'] = data.Likes.objects.filter(liked_type=ele_type, liked_id=ele_dict['id']).count()
        ele_dict['follows'] = data.Follows.objects.filter(liked_type=ele_type, liked_id=ele_dict['id']).count()

        ele_dict['ele_liked'] = False
        ele_dict['ele_followed'] = False
        if ses.get('user_id'):
            if data.Likes.objects.filter(hosts=get_user_by_id(ses['user_id']),
                                         liked_type=ele_type, liked_id=ele_dict['id']).count() == 1:
                ele_dict['ele_liked'] = True
            if data.Follows.objects.filter(following=get_user_by_id(ses['user_id']),
                                           followed_type=ele_type, followed_id=ele_dict['id']).count() == 1:
                ele_dict['ele_followed'] = True

        comments_list = get_comments_list(space, ele_dict['id'], ele_type)
        for each in comments_list:
            commenter = data.User.objects.filter(id=each['user_id'])
            if commenter.count() != 1:
                return JsonResponse({
                    'errno': '402',
                    'msg': '评论者id不存在'})
            each['commenter'] = model_to_dict(commenter)

        is_like = request.POST.get('is_like')
        is_follow = request.POST.get('is_follow')
        is_like_element = request.POST.get('is_like_element')
        is_follow_element = request.POST.get('is_follow_element')
        return like_follow_element(space, ses, is_like, is_follow, is_like_element, is_follow_element,
                                   ret_dict, ele_type, ele_dict, comments_list)
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


@csrf_exempt
def space_notices(request, space_id, notices_id):
    if request.method == 'POST':
        ses = request.session
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})
        notice = data.SpaceNotices.objects.filter(id=notices_id)
        if notice.count() != 1:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到待删除资源'})
        notice = notice[0]
        ret_dict = init_ret_dict(ses, space)

        is_delete = request.POST.get('is_delete')
        if is_delete:
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})

            if notice.user_id != ses.get('user_id'):
                return JsonResponse({
                    'errno': '407',
                    'msg': '待删除习题不是当前用户所创建'})
            notice.delete()
            return JsonResponse({
                'errno': '200',
                'msg': '删除成功'})

        ele_type = '公告'
        ele_dict = model_to_dict(notice)

        is_like = request.POST.get('is_like')
        is_follow = request.POST.get('is_follow')
        return like_follow_element(space, ses, is_like, is_follow, False, False,
                                   ret_dict, ele_type, ele_dict, None)
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


'''
需要的参数：
is_edit: 代表用户是否点击了提交编辑按钮（进入该路由不一定就是已经编辑完毕了） True/1代表是
resource_name:string，没有改变可以不传、传null、传原数据
introduction:string，没有改变可以不传、传null、传原数据
file:资源文件，没有改变就不要传
返回数据：
data：ret_dict
old_element：原资源字典（编辑以前最好显示原资源的内容）
'''


@csrf_exempt
def space_resources_edit(request, space_id, resources_id):
    if request.method == 'POST':
        ses = request.session
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'
            })
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})
        resource = data.SpaceResources.objects.filter(id=resources_id)
        if resource.count() != 1:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到资源'})
        ret_dict = init_ret_dict(ses, space)
        resource = resource[0]
        ele_type = '资源'
        ele_dict = model_to_dict(resource, exclude=['file'])

        is_edit = request.POST.get('is_edit')
        if is_edit is None:
            return JsonResponse({
                'errno': '200',
                'msg': '查询原元素成功',
                'data': ret_dict,
                'old_element': ele_dict,
            })
        if is_edit == '1':
            resource_name = request.POST.get('resource_name')
            introduction = request.POST.get('introduction')
            file = request.FILES.get('file')
            if resource_name:
                resource.resource_name = resource_name
            if introduction:
                resource.introduction = introduction
            if file is not None:
                resource.file = file
            resource.last_update_time = get_time_now()
            resource.save()
            return JsonResponse({
                'errno': '200',
                'msg': '编辑元素成功',
                'data': ret_dict,
            })
        else:
            return JsonResponse({
                'errno': '200',
                'msg': '查询原元素成功',
                'data': ret_dict,
                'old_element': ele_dict,
            })

    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


'''
需要的参数：
is_create: int
resource_name
introduction
file
返回数据：

'''


@csrf_exempt
def space_resources_create(request, space_id):
    if request.method == 'POST':
        ses = request.session
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'
            })
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})

        ret_dict = init_ret_dict(ses, space)
        is_create = request.POST.get('is_create')
        if not is_create:
            return JsonResponse({
                'errno': '200',
                'msg': '等待创建',
                'data': ret_dict
            })

        resource_name = request.POST.get('resource_name')
        introduction = request.POST.get('introduction')
        file = request.FILES.get('file')
        ret = exist_check(resource_name, introduction, file)
        time_now = get_time_now()
        if ret is not None:
            return ret
        new_resource = data.SpaceResources(
            space_id=space,
            user_id=get_user_by_id(ses['user_id']),
            resource_name=resource_name,
            introduction=introduction,
            file=file,
            create_time=time_now,
            last_update_time=time_now
        )
        new_resource.save()
        activities_add(ses['user_id'], 0, "资源", space.id, new_resource.id, '创建了资源')
        return JsonResponse({
            'errno': '200',
            'msg': '创建元素成功',
            'data': ret_dict,
        })
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


@csrf_exempt
def space_questions_edit(request, space_id, questions_id):
    if request.method == 'POST':
        ses = request.session
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'
            })
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})
        question = data.SpaceQuestions.objects.filter(id=questions_id)
        if question.count() != 1:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到讨论'})
        ret_dict = init_ret_dict(ses, space)
        question = question[0]
        ele_type = '讨论'
        ele_dict = model_to_dict(question)

        is_edit = request.POST.get('is_edit')
        if is_edit is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少is_edit'})
        if is_edit:
            title = request.POST.get('title')
            content = request.POST.get('content')
            if title:
                question.title = title
            if content:
                question.content = content
            question.last_update_time = get_time_now()
            question.save()

            return JsonResponse({
                'errno': '200',
                'msg': '编辑成功',
                'data': ret_dict,
            })
        else:
            return JsonResponse({
                'errno': '200',
                'msg': '查询原元素成功',
                'data': ret_dict,
                'old_element': ele_dict,
            })

    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


'''
is_create
title
content
'''


@csrf_exempt
def space_questions_create(request, space_id):
    if request.method == 'POST':
        ses = request.session
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'
            })
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})

        ret_dict = init_ret_dict(ses, space)
        is_create = request.POST.get('is_create')
        if not is_create:
            return JsonResponse({
                'errno': '200',
                'msg': '等待创建',
                'data': ret_dict
            })

        title = request.POST.get('title')
        content = request.POST.get('content')
        ret = exist_check(title, content)
        time_now = get_time_now()
        if ret is not None:
            return ret
        new_question = data.SpaceQuestions(
            space_id=space,
            user_id=get_user_by_id(ses['user_id']),
            title=title,
            content=content,
            create_time=time_now,
            last_update_time=time_now
        )
        new_question.save()
        activities_add(ses['user_id'], 0, "讨论", space.id, new_question.id, '创建了讨论')
        return JsonResponse({
            'errno': '200',
            'msg': '创建元素成功',
            'data': ret_dict,
        })
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


'''
is_edit
exercise_type
content
difficulty
answer
'''


@csrf_exempt
def space_exercises_edit(request, space_id, exercises_id):
    if request.method == 'POST':
        ses = request.session
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'
            })
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})
        exercise = data.SpaceExercises.objects.filter(id=exercises_id)
        if exercise.count() != 1:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到讨论'})
        ret_dict = init_ret_dict(ses, space)
        exercise = exercise[0]
        ele_type = '习题'
        ele_dict = model_to_dict(exercise)

        is_edit = request.POST.get('is_edit')
        if is_edit is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少is_edit'})
        if is_edit:

            content = request.POST.get('content')
            exercise_type = request.POST.get('type')
            difficulty = request.POST.get('difficulty')
            answer = request.POST.get('answer')
            if content:
                exercise.content = content
            if exercise_type:
                exercise.type = exercise_type
            if difficulty:
                exercise.difficulty = difficulty
            if answer:
                exercise.answer = answer
            exercise.last_update_time = get_time_now()
            exercise.save()

            return JsonResponse({
                'errno': '200',
                'msg': '编辑成功',
                'data': ret_dict,
            })
        else:
            return JsonResponse({
                'errno': '200',
                'msg': '查询原元素成功',
                'data': ret_dict,
                'old_element': ele_dict,
            })

    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


'''
is_create
exercise_type
content
difficulty
answer
'''


@csrf_exempt
def space_exercises_create(request, space_id):
    if request.method == 'POST':
        ses = request.session
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'
            })
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})

        ret_dict = init_ret_dict(ses, space)
        is_create = request.POST.get('is_create')
        if not is_create:
            return JsonResponse({
                'errno': '200',
                'msg': '等待创建',
                'data': ret_dict
            })

        exercise_type = request.POST.get('type')
        content = request.POST.get('content')
        difficulty = request.POST.get('difficulty')
        answer = request.POST.get('answer')
        ret = exist_check(exercise_type, content, difficulty, answer)
        time_now = get_time_now()
        if ret is not None:
            return ret
        new_question = data.SpaceQuestions(
            space_id=space,
            user_id=get_user_by_id(ses['user_id']),
            content=content,
            type=exercise_type,
            difficulty=difficulty,
            answer=answer,
            create_time=time_now,
            last_update_time=time_now
        )
        new_question.save()
        activities_add(ses['user_id'], 0, "练习", space.id, new_question.id, '创建了练习')
        return JsonResponse({
            'errno': '200',
            'msg': '创建元素成功',
            'data': ret_dict,
        })
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


def space_groups_edit(request, space_id, groups_id):
    return 0


def space_groups_create(request, space_id):
    return 0


@csrf_exempt
def space_notices_edit(request, space_id, notices_id):
    if request.method == 'POST':
        ses = request.session
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'
            })
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})
        notice = data.SpaceNotices.objects.filter(id=notices_id)
        if notice.count() != 1:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到讨论'})
        ret_dict = init_ret_dict(ses, space)
        notice = notice[0]
        ele_type = '讨论'
        ele_dict = model_to_dict(notice)

        is_edit = request.POST.get('is_edit')
        if is_edit is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少is_edit'})
        if is_edit:
            title = request.POST.get('title')
            content = request.POST.get('content')
            ret = exist_check(title, content)
            if ret is not None:
                return ret
            notice.last_update_time = get_time_now()
            notice.save()

            return JsonResponse({
                'errno': '200',
                'msg': '编辑成功',
                'data': ret_dict,
            })
        else:
            return JsonResponse({
                'errno': '200',
                'msg': '查询原元素成功',
                'data': ret_dict,
                'old_element': ele_dict,
            })

    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


@csrf_exempt
def space_notices_create(request, space_id):
    if request.method == 'POST':
        ses = request.session
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'
            })
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 0:
            return JsonResponse({
                'errno': '403',
                'msg': '非私有学习空间成员'})

        ret_dict = init_ret_dict(ses, space)
        is_create = request.POST.get('is_create')
        if not is_create:
            return JsonResponse({
                'errno': '200',
                'msg': '等待创建',
                'data': ret_dict
            })

        title = request.POST.get('title')
        content = request.POST.get('content')
        ret = exist_check(title, content)
        time_now = get_time_now()
        if ret is not None:
            return ret
        new_notice = data.SpaceNotices(
            space_id=space,
            user_id=get_user_by_id(ses['user_id']),
            title=title,
            content=content,
            create_time=time_now,
            last_update_time=time_now
        )
        new_notice.save()
        return JsonResponse({
            'errno': '200',
            'msg': '创建元素成功',
            'data': ret_dict,
        })
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


'''
需要的参数
edit_normal: 1/0
new_name:
new_introduction:
edit_member: 1/0
add_member: 1/0
key: string，管理员输入邀请码则邀请对应用户加入
edit_admin: 1/0
add_admin: 1/0
generate_key: 1/0，生成用户专属邀请码
member_id: 成员id，如果存在则从对应列表删除，如果是添加管理员则添加该用户
edit_high: 1/0
'''


@csrf_exempt
def space_setting(request, space_id):
    if request.method == 'POST':
        ses = request.session
        if ses.get('user_id') is None:
            return JsonResponse({
                'errno': '400',
                'msg': '尚未登录'
            })
        space = data.StudySpaces.objects.filter(id=space_id)
        if space.count() == 0:
            return JsonResponse({
                'errno': '404',
                'msg': '未找到学习空间'})
        space = space[0]
        perm = space_permissions_check(ses, space)
        if perm <= 1:
            return JsonResponse({
                'errno': '403',
                'msg': '非管理员不可修改空间'})

        ret_dict = init_ret_dict(ses, space)
        if request.POST.get('edit_normal') == '1':
            return 0
        elif request.POST.get('edit_member') == '1':
            return 0
        elif request.POST.get('edit_admin') == '1':
            if perm <= 2:
                return JsonResponse({
                    'errno': '403',
                    'msg': '非创建者不可修改空间管理员'})
        elif request.POST.get('edit_high') == '1':
            if perm <= 2:
                return JsonResponse({
                    'errno': '403',
                    'msg': '非创建者不可修改空间高级设置'})
        else:
            return JsonResponse({
                'errno': '200',
                'msg': '进入设置页面成功',
                'data': ret_dict,
            })

    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
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


# 需要：用户名、密码、确认密码、邮箱
@csrf_exempt
def user_confirm(request):
    if request.method == 'POST':
        code = request.POST.get('code')
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


# 输入验证码
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # 获取请求数据
        password = request.POST.get('password')


        try:
            # print(email)
            user = User.objects.get(email=email)
        except:
            return JsonResponse({'error': 1011, 'msg': "没有此用户"})

        if request.session.get('uid') == user.id:
            return JsonResponse({'error': 1009, 'msg': "已经登录"})

        if user.password == password:  # 判断请求的密码是否与数据库存储的密码相同
            if not user.confirmed:
                return JsonResponse({'error': 1010, 'msg': "未确认"})
            request.session['uid'] = user.id  # 密码正确则将用户名存储于session（django用于存储登录信息的数据库位置）
            request.session['user_id'] = user.id
            return JsonResponse({'error': 1, 'msg': "登录成功"})
        else:
            return JsonResponse({'error': 1002, 'msg': "密码错误"})
    else:
        return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


# 填入用户名和密码

@csrf_exempt
def logout(request):
    del request.session['uid']
    del request.session['user_id']
    return JsonResponse({'error': 1, 'msg': "注销成功"})


@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        old_password = request.POST.get('password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
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


# 改变密码

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

        username = request.POST.get('username')
        gender = request.POST.get('gender')
        tags = request.POST.get('tags')
        destination = request.POST.get('destination')
        job = request.POST.get('job')
        organization = request.POST.get('organization')
        intro = request.POST.get('intro')

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
        activities = Activities.objects.filter(hosts=uid)

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
        studyspaces = StudySpaces.objects.filter(creator_id=get_user_by_id(uid))

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
            u = User.objects.get(id=uid)
        except:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})
        follows = SpaceFollows.objects.filter(user_id=u)
        studyspaces = []

        for follow in follows:
            studyspaces.append(follow.space_id)
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
        except Exception:
            return JsonResponse({'error': 1014, 'msg': "没有相应用户"})

        resources = SpaceResources.objects.filter(user_id=uid)
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
        questions = SpaceQuestions.objects.filter(user_id=uid)

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
        answers = SpaceComments.objects.filter(user_id=uid, comment_type='answer')

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
        exercises = SpaceExercises.objects.filter(user_id=uid)

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
        collects = Follows.objects.filter(followed_type='资源', following=get_user_by_id(uid))

        resources_need = []

        for collect in collects:
            r_id = collect.followed_id
            resource = SpaceResources.objects.get(id=r_id)
            studyspace = StudySpaces.objects.get(id=resource.space_id.id)
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
        collects = Follows.objects.filter(followed_type='讨论', following=get_user_by_id(uid))

        questions_need = []

        for collect in collects:
            q_id = collect.followed_id
            question = SpaceQuestions.objects.get(id=q_id)
            studyspace = StudySpaces.objects.get(id=question.space_id.id)
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
        collects = Follows.objects.filter(followed_type='评论', following=get_user_by_id(uid))

        answers_need = []

        for collect in collects:
            a_id = collect.followed_id
            answer = SpaceComments.objects.get(id=a_id)
            studyspace = StudySpaces.objects.filter(id=answer.space_id.id)
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
        collects = Follows.objects.filter(followed_type='练习', following=get_user_by_id(uid))

        exercises_need = []

        for collect in collects:
            e_id = collect.followed_id
            exercise = SpaceExercises.objects.get(id=e_id)
            studyspace = StudySpaces.objects.get(id=exercise.space_id.id)
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
        follows = Follows.objects.filter(following=uid, followed_type='people')

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
        follows = Follows.objects.filter(followed_id=uid, followed_type='people')

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
            activities_add(user_id, 0, '用户', uid, 0, '关注了用户')

            return JsonResponse({'error': 1, 'msg': '关注成功'})

        fan.followings -= 1
        follow.followers -= 1
        follow.delete()
        follow.id = uid
        follow.save()
        return JsonResponse({'error': 1, 'msg': '取消关注成功'})

    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def search(request):
    if request.method == 'GET':
        recv = request.POST
        types = recv.get('types')  # 搜索类型
        text = recv.get('text')  # 搜索内容
        method = recv.get('method')  # 搜索排序方式
        if method is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少order'})
        order = {}

        if types == 'spaces':
            if method == '最多点赞':
                order = 'id'
            elif method == '最多关注':
                order = 'id'
            elif method == '最近更新':
                order = '-last_update_time'
            elif method == '最早更新':
                order = 'last_update_time'
            elif method == '最近创建':
                order = '-create_time'
            elif method == '最早创建':
                order = 'create_time'
            else:
                return JsonResponse({
                    'errno': '401',
                    'msg': 'POST参数order不合法'})
            studyspaces = StudySpaces.objects.filter(Q(space_introduction__icontains=text)
                                                     | Q(space_name__icontains=text)).order_by(order)
            studyspaces_need = []
            for each in studyspaces:
                each_dict = model_to_dict(each, exclude=['space_picture'])
                each_dict['likes'] = data.SpaceLikes.objects.filter(space_id=each_dict['id']).count()
                each_dict['follows'] = data.SpaceFollows.objects.filter(space_id=each_dict['id']).count()
                studyspaces_need.append(each_dict)
            studyspaces_need = order_query_list(studyspaces_need, method)
            return JsonResponse({'error': 1, 'msg': '搜索空间成功', 'data': studyspaces_need})

        elif types == 'resources':
            if method == '最多点赞':
                order['orderby_table'] = 'SpaceResources'
                order['orderby_object'] = 'resources_likes'
                order['orderby'] = ''  # 升序
            elif method == '最多评论':
                order['orderby_table'] = 'SpaceResources'
                order['orderby_object'] = 'resources_comments'
                order['orderby'] = ''  # 升序
            elif method == '最近更新':
                order['orderby_table'] = 'SpaceResources'
                order['orderby_object'] = 'last_update_time'
                order['orderby'] = '-'  # 降序
            elif method == '最早更新':
                order['orderby_table'] = 'SpaceResources'
                order['orderby_object'] = 'last_update_time'
                order['orderby'] = ''  # 升序
            elif method == '最近创建':
                order['orderby_table'] = 'SpaceResources'
                order['orderby_object'] = 'create_time'
                order['orderby'] = '-'  # 降序
            elif method == '最早创建':
                order['orderby_table'] = 'SpaceResources'
                order['orderby_object'] = 'create_time'
                order['orderby'] = ''  # 升序
            else:
                return JsonResponse({
                    'errno': '401',
                    'msg': 'POST参数order不合法'})
            resources = SpaceResources.objects.filter(file_name__icontains=text).order_by(
                order['orderby'] +
                order['orderby_table'] + '__' +
                order['orderby_object']
            )
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
            return JsonResponse({'error': 1, 'msg': '搜索资源成功', 'data': resources_need})

        elif types == 'questions':
            if method == '最多点赞':
                order['orderby_table'] = 'SpaceQuestions'
                order['orderby_object'] = 'questions_likes'
                order['orderby'] = ''  # 升序
            elif method == '最多评论':
                order['orderby_table'] = 'SpaceQuestions'
                order['orderby_object'] = 'questions_comments'
                order['orderby'] = ''  # 升序
            elif method == '最近更新':
                order['orderby_table'] = 'SpaceQuestions'
                order['orderby_object'] = 'last_update_time'
                order['orderby'] = '-'  # 降序
            elif method == '最早更新':
                order['orderby_table'] = 'SpaceQuestions'
                order['orderby_object'] = 'last_update_time'
                order['orderby'] = ''  # 升序
            elif method == '最近创建':
                order['orderby_table'] = 'SpaceQuestions'
                order['orderby_object'] = 'create_time'
                order['orderby'] = '-'  # 降序
            elif method == '最早创建':
                order['orderby_table'] = 'SpaceQuestions'
                order['orderby_object'] = 'create_time'
                order['orderby'] = ''  # 升序
            else:
                return JsonResponse({
                    'errno': '401',
                    'msg': 'POST参数order不合法'})

            questions = SpaceQuestions.objects.filter(Q(title__icontains=text)
                                                      | Q(content__icontains=text)).order_by(order)
            questions_need = []
            for question in questions:
                studyspace = StudySpaces.objects.get(id=question.space_id)
                user_act = {
                    "id": question.id,
                    "space_name": studyspace.space_name,
                    "question_title": question.title,
                    "create_time": question.create_time,
                    "from_space_id": studyspace.id,
                    "uid": studyspace.creator_id,
                }
                questions_need.append(user_act)
            return JsonResponse({'error': 1, 'msg': '搜索提问成功', 'data': questions_need})

        elif types == 'exercises':
            if method == '最多点赞':
                order['orderby_table'] = 'SpaceExercises'
                order['orderby_object'] = 'exercises_likes'
                order['orderby'] = ''  # 升序
            elif method == '最多评论':
                order['orderby_table'] = 'SpaceExercises'
                order['orderby_object'] = 'exercises_comments'
                order['orderby'] = ''  # 升序
            elif method == '最近更新':
                order['orderby_table'] = 'SpaceExercises'
                order['orderby_object'] = 'last_update_time'
                order['orderby'] = '-'  # 降序
            elif method == '最早更新':
                order['orderby_table'] = 'SpaceExercises'
                order['orderby_object'] = 'last_update_time'
                order['orderby'] = ''  # 升序
            elif method == '最近创建':
                order['orderby_table'] = 'SpaceExercises'
                order['orderby_object'] = 'create_time'
                order['orderby'] = '-'  # 降序
            elif method == '最早创建':
                order['orderby_table'] = 'SpaceExercises'
                order['orderby_object'] = 'create_time'
                order['orderby'] = ''  # 升序
            else:
                return JsonResponse({
                    'errno': '401',
                    'msg': 'POST参数order不合法'})

            exercises = SpaceExercises.objects.filter(Q(type=text)
                                                      | Q(content__icontains=text)).order_by(
                order['orderby'] +
                order['orderby_table'] + '__' +
                order['orderby_object']
            )
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
                    "uid": studyspace.creator_id,
                }
                exercises_need.append(user_act)
            return JsonResponse({'error': 1, 'msg': '搜索习题成功', 'data': exercises_need})
        elif types == 'users':
            users = User.objects.filter(username__icontains=text)
            user_need = []

            for user in users:
                user_act = {
                    "uid": user.id,
                    "username": user.username
                }
                user_need.append(user_act)
            return JsonResponse({'error': 1, 'msg': '搜索用户成功', 'data': user_need})
        else:
            return JsonResponse({'error': 1016, 'msg': "搜索方式错误"})
    return JsonResponse({'error': 1001, 'msg': "请求方式错误"})


def activities_add(user_id, create_time, objects_type, t_id, s_id, contents):
    user = User.objects.get(id=user_id)
    new_activities = Activities()
    if objects_type == '用户':
        create_time = get_time_now()
        s_id = 0
    new_activities.hosts = user
    new_activities.create_time = create_time
    new_activities.type = objects_type
    new_activities.s_id = s_id
    new_activities.t_id = t_id
    new_activities.programs = contents

    new_activities.save()
    return 0
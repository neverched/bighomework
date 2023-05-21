import os

from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import app01.models as data
import time


# Create your views here.


def get_time_now():
    create_time = time.localtime(time.time())
    create_time = str(create_time.tm_year) + "-" + str(create_time.tm_mon) + "-" + \
                  str(create_time.tm_mday) + " " + str(create_time.tm_hour) + ":" + \
                  str(create_time.tm_min) + ":" + str(create_time.tm_sec)
    return create_time


def order_query_list(query_list, method):
    if method == '最多点赞':
        query_list.sort(key=lambda k: (k.get('likes', 0)), reverse=True)
    elif method == '最多关注':
        query_list.sort(key=lambda k: (k.get('follows', 0)), reverse=True)
    return query_list


# 3是创建者，2是管理员，1是可访问普通用户，0是不可访问
def space_permissions_check(ses, space):
    if space.creator_id == ses.get('user_id'):
        return 3
    perm = space.space_permission
    member = data.SpaceMembers.objects.filter(space_id=space.id, user_id=ses.get('user_id')).count()
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
    comments_set = data.SpaceComments.objects.filter(space_id=space.id, element_id=ele_id, comment_type=ele_type)
    c_list = []
    for each in comments_set:
        each_dict = model_to_dict(each)
        each_dict['likes'] = data.Likes.objects.filter(liked_id=ele_id, liked_type=ele_type).count()
        each_dict['follows'] = data.Follows.objects.filter(followed_id=ele_id, followed_type=ele_type).count()
        c_list.append(each_dict)
    return c_list


def init_ret_dict(ses, space):
    admin_set = data.SpaceMembers.objects.filter(space_id=space.id, is_admin=1)
    creator = data.User.objects.filter(id=space.creator_id)
    admin_list = [model_to_dict(creator)]
    for each in admin_set:
        each_dict = model_to_dict(each)
        admin_list.append(each_dict)
    ret_dict = {'space_name': space.space_name, 'space_index': space.space_index,
                'space_introduction': space.space_introduction, 'space_picture': space.space_picture,
                'create_time': space.create_time,
                'likes_num': data.SpaceLikes.objects.filter(space_id=space.id).count(),
                'follows_num': data.SpaceFollows.objects.filter(space_id=space.id).count(),
                'resources_num': data.SpaceResources.objects.filter(space_id=space.id).count(),
                'exercises_num': data.SpaceExercises.objects.filter(space_id=space.id).count(),
                'questions_num': data.SpaceQuestions.objects.filter(space_id=space.id).count(),
                'groups_num': data.SpaceGroups.objects.filter(space_id=space.id).count(),
                'notices_num': data.SpaceNotices.objects.filter(space_id=space.id).count(),
                'admin_list': admin_list,
                'user_permission': space_permissions_check(ses, space),
                'liked': False,
                'followed': False,
                }
    return ret_dict


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
        order = {}
        method = recv.get('order')
        if method is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少order'})
        elif method == '最多点赞':
            order['orderby_table'] = 'StudySpaces'
            order['orderby_object'] = 'pk'
            order['orderby'] = ''  # 升序
        elif method == '最多关注':
            order['orderby_table'] = 'StudySpaces'
            order['orderby_object'] = 'pk'
            order['orderby'] = ''  # 升序
        elif method == '最近更新':
            order['orderby_table'] = 'StudySpaces'
            order['orderby_object'] = 'last_update_time'
            order['orderby'] = '-'  # 降序
        elif method == '最早更新':
            order['orderby_table'] = 'StudySpaces'
            order['orderby_object'] = 'last_update_time'
            order['orderby'] = ''  # 升序
        elif method == '最近创建':
            order['orderby_table'] = 'StudySpaces'
            order['orderby_object'] = 'create_time'
            order['orderby'] = '-'  # 降序
        elif method == '最早创建':
            order['orderby_table'] = 'StudySpaces'
            order['orderby_object'] = 'create_time'
            order['orderby'] = ''  # 升序
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
        query_list = []
        if recv.get('show') == '全部空间':
            query_set = data.StudySpaces.objects.all.order_by(order['orderby'] +
                                                              order['orderby_table'] + '__' +
                                                              order['orderby_object'])
            for each in query_set:
                each_dict = model_to_dict(each)
                each_dict['likes'] = data.SpaceLikes.objects.filter(space_id=each_dict['id']).count()
                each_dict['follows'] = data.SpaceFollows.objects.filter(space_id=each_dict['id']).count()
                query_list.append(each_dict)
            total = len(query_list)
            query_list = order_query_list(query_list, method)
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
            id_list = data.SpaceLooks.objects.filter(user_id=ses['user_id']).values('space_id')
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
            id_set = data.Follows.objects.filter(user_id=ses['user_id']).values('space_id')
            space_set = data.StudySpaces.objects.all.order_by(order['orderby'] +
                                                              order['orderby_table'] + '__' +
                                                              order['orderby_object'])
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
            space_set = data.StudySpaces.objects.filter(user_id=ses['user_id']).order_by(order['orderby'] +
                                                                                         order['orderby_table'] + '__' +
                                                                                         order['orderby_object'])
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
                                         last_update_time=create_time)
        else:
            extended_name = os.path.splitext(space_picture.name)[-1]
            allowed_name = ['.jpg', '.png']
            if extended_name not in allowed_name:
                return JsonResponse({
                    'errno': '402',
                    'msg': '上传图片后缀名不合法'})
            file_data = space_picture.read()
            new_space = data.StudySpaces(space_name=space_name,
                                         space_introduction=space_introduction,
                                         space_permission=space_permission,
                                         create_time=create_time,
                                         last_update_time=create_time,
                                         space_picture=file_data)
        try:
            new_space.save()
        except RuntimeError:
            return JsonResponse({
                'errno': '403',
                'msg': '数据库操作失败'})
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
        ses = request.sessions
        space = data.StudySpaces.objects.filter(space_id=space_id)
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
            liked = data.SpaceLikes.objects.filter(space_id=space.id, user_id=ses['user_id']).count()
            if liked == 1:
                ret_dict['liked'] = True
            followed = data.SpaceFollows.objects.filter(space_id=space.id, user_id=ses['user_id']).count()
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
                data.SpaceLikes.objects.filter(space_id=space.id, user_id=ses['user_id']).delete()
                ret_dict['liked'] = False
            else:
                data.SpaceLikes.objects.create(space_id=space.id, user_id=ses['user_id'], like_time=get_time_now())
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
                data.SpaceFollows.objects.filter(space_id=space.id, user_id=ses['user_id']).delete()
                ret_dict['followed'] = False
            else:
                data.SpaceFollows.objects.create(space_id=space.id, user_id=ses['user_id'], like_time=get_time_now())
                ret_dict['followed'] = True
        else:
            return JsonResponse({
                'errno': '200',
                'msg': '收藏/取消收藏成功',
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
        ses = request.sessions
        space = data.StudySpaces.objects.filter(space_id=space_id)
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
        query_list = []
        method = request.POST.get('order')
        order = {}
        if method is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少order'})
        elif method == '最多点赞':
            order['orderby_table'] = 'SpaceResources'
            order['orderby_object'] = 'pk'
            order['orderby'] = ''  # 降序
        elif method == '资源标题':
            order['orderby_table'] = 'SpaceResources'
            order['orderby_object'] = 'resource_name'
            order['orderby'] = '-'  # 降序
        elif method == '最近更新':
            order['orderby_table'] = 'SpaceResources'
            order['orderby_object'] = 'last_update_time'
            order['orderby'] = '-'  # 降序
        elif method == '最早更新':
            order['orderby_table'] = 'SpaceResources'
            order['orderby_object'] = 'last_update_time'
            order['orderby'] = ''  # 升序
        else:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数order不合法'})
        resources_set = data.SpaceResources.objects.filter(space_id=space.id).order_by(order['orderby'] +
                                                                                       order['orderby_table'] + '__' +
                                                                                       order['orderby_object'])
        total = resources_set.count()
        for each in resources_set:
            each_dict = model_to_dict(each)
            each_dict['likes'] = data.Likes.objects.filter(like_type='资源', liked_id=each_dict['id']).count()
            each_dict['follows'] = data.Follows.objects.filter(like_type='资源', liked_id=each_dict['id']).count()
            query_list.append(each_dict)
        query_list = order_query_list(query_list, method)

        is_like = request.POST.get('is_like')
        is_follow = request.POST.get('is_follow')

        if ses.get('user_id') is not None:
            liked = data.SpaceLikes.objects.filter(space_id=space.id, user_id=ses['user_id']).count()
            if liked == 1:
                ret_dict['liked'] = True
            followed = data.SpaceFollows.objects.filter(space_id=space.id, user_id=ses['user_id']).count()
            if followed == 1:
                ret_dict['followed'] = True

        if is_like:
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})
            if ret_dict['liked']:
                data.SpaceLikes.objects.filter(space_id=space.id, user_id=ses['user_id']).delete()
                ret_dict['liked'] = False
            else:
                data.SpaceLikes.objects.create(space_id=space.id, user_id=ses['user_id'], like_time=get_time_now())
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
                data.SpaceFollows.objects.filter(space_id=space.id, user_id=ses['user_id']).delete()
                ret_dict['followed'] = False
            else:
                data.SpaceFollows.objects.create(space_id=space.id, user_id=ses['user_id'], like_time=get_time_now())
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
                'msg': '查询资源成功',
                'data': ret_dict,
                'list': query_list[page * 10 - 10:page * 10 - 1],
                'total': total
            })

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
        ses = request.sessions
        space = data.StudySpaces.objects.filter(space_id=space_id)
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
        query_list = []
        groups_set = data.SpaceGroups.objects.filter(space_id=space.id)
        total = groups_set.count()
        for each in groups_set:
            each_dict = model_to_dict(each)
            each_dict['member_num'] = each.members.count()
            query_list.append(each_dict)
        if ses.get('user_id') is not None:
            liked = data.SpaceLikes.objects.filter(space_id=space.id, user_id=ses['user_id']).count()
            if liked == 1:
                ret_dict['liked'] = True
            followed = data.SpaceFollows.objects.filter(space_id=space.id, user_id=ses['user_id']).count()
            if followed == 1:
                ret_dict['followed'] = True
        is_like = request.POST.get('is_like')
        is_follow = request.POST.get('is_follow')

        if is_like:
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})
            if ret_dict['liked']:
                data.SpaceLikes.objects.filter(space_id=space.id, user_id=ses['user_id']).delete()
                ret_dict['liked'] = False
            else:
                data.SpaceLikes.objects.create(space_id=space.id, user_id=ses['user_id'], like_time=get_time_now())
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
                data.SpaceFollows.objects.filter(space_id=space.id, user_id=ses['user_id']).delete()
                ret_dict['followed'] = False
            else:
                data.SpaceFollows.objects.create(space_id=space.id, user_id=ses['user_id'], like_time=get_time_now())
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
                'msg': '查询群组成功',
                'data': ret_dict,
                'list': query_list[page * 10 - 10:page * 10 - 1],
                'total': total
            })
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


def space_questions_index(request, space_id):
    if request.method == 'POST':
        ses = request.sessions
        space = data.StudySpaces.objects.filter(space_id=space_id)
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

        method = request.POST.get('order')
        order = {}
        if method is None:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数缺少order'})
        elif method == '最多点赞':
            order['orderby_table'] = 'SpaceQuestions'
            order['orderby_object'] = 'pk'
            order['orderby'] = ''
        elif method == '最多讨论':
            order['orderby_table'] = 'SpaceQuestions'
            order['orderby_object'] = 'pk'
            order['orderby'] = ''
        elif method == '最近更新':
            order['orderby_table'] = 'SpaceQuestions'
            order['orderby_object'] = 'last_update_time'
            order['orderby'] = '-'
        elif method == '最新创建':
            order['orderby_table'] = 'SpaceQuestions'
            order['orderby_object'] = 'create_time'
            order['orderby'] = '-'
        else:
            return JsonResponse({
                'errno': '401',
                'msg': 'POST参数order不合法'})

        query_list = []
        questions_set = data.SpaceQuestions.objects.filter(space_id=space_id).order_by(order['orderby'] +
                                                                                       order['orderby_table'] + '__' +
                                                                                       order['orderby_object'])
        total = questions_set.count()
        for each in questions_set:
            each_dict = model_to_dict(each)





    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


def space_exercises_index(request, space_id):
    if request.method == 'POST':
        ses = request.sessions
        space = data.StudySpaces.objects.filter(space_id=space_id)
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
        query_list = []
        exercises_set = data.SpaceResources.objects.filter(space_id=space_id)
        total = exercises_set.count()

    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


def space_notices_index(request, space_id):
    if request.method == 'POST':
        return 0
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


'''
需要的参数：
is_like: int 代表是否点击了点赞按钮，True/1代表是
is_follow: int 代表是否点击了收藏按钮，True/1代表是
is_edit: int 代表是否申请编辑自己创建的资源内容，True/1代表是
is_delete: int 代表是否申请删除自己创建的资源内容，True/1代表是
is_like_element: int 代表是否是点击了点赞资源按钮，True/1代表是
（以上五个至多一个True，学习空间除了创建界面任何位置都能点击点赞收藏按钮）

返回内容
data：ret_dict
element：该资源的字典
comments_list：该资源的评论字典列表，新加key：commenter 评论者的用户字典（还没写，如果觉得麻烦我就拿出来，字典里面的字典确实难访问）
'''


@csrf_exempt
def space_resources(request, space_id, resources_id):
    if request.method == 'POST':
        ses = request.sessions
        space = data.StudySpaces.objects.filter(space_id=space_id)
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
        is_delete = request.POST.get('is_delete')

        if is_delete:
            if ses.get('user_id') is None:
                return JsonResponse({
                    'errno': '400',
                    'msg': '尚未登录'})
            resource_deleted = data.SpaceResources.objects.filter(id=resources_id)
            if resource_deleted.count() != 1:
                return JsonResponse({
                    'errno': '404',
                    'msg': '未找到待删除资源'})
            if resource_deleted[0].user_id != ses.get('user_id'):
                return JsonResponse({
                    'errno': '407',
                    'msg': '待删除资源不是当前用户所创建'})
            resource_deleted.delete()
            return JsonResponse({
                'errno': '200',
                'msg': '删除成功'})



    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


def space_questions(request, space_id, questions_id):
    if request.method == 'POST':
        return 0
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


def space_exercises(request, space_id, exercises_id):
    if request.method == 'POST':
        return 0
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


def space_groups(request, space_id, groups_id):
    if request.method == 'POST':
        return 0
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


def space_notices(request, space_id, notices_id):
    if request.method == 'POST':
        return 0
    else:
        return JsonResponse({
            'errno': '405',
            'msg': '请求方式错误'})


def space_resources_edit(request, space_id, resources_id):
    return 0


def space_resources_create(request, space_id, resources_id):
    return 0


def space_questions_edit(request, space_id, resources_id):
    return 0


def space_questions_create(request, space_id, resources_id):
    return 0


def space_exercises_edit(request, space_id, resources_id):
    return 0


def space_exercises_create(request, space_id, resources_id):
    return 0


def space_groups_edit(request, space_id, resources_id):
    return 0


def space_groups_create(request, space_id, resources_id):
    return 0


def space_notices_edit(request, space_id, resources_id):
    return 0


def space_notices_create(request, space_id, resources_id):
    return 0

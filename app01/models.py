from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256, default="")
    gender = models.IntegerField(default=0)
    intro = models.CharField(max_length=256, default="")
    organization = models.CharField(max_length=50, verbose_name="所属组织", default="")
    destination = models.CharField(max_length=256, default="")
    job = models.CharField(max_length=256, default="")
    followers = models.IntegerField(default=0, verbose_name="粉丝数")
    followings = models.IntegerField(default=0, verbose_name="关注数")
    like = models.IntegerField(default=0, verbose_name="点赞数")
    tags = models.CharField(max_length=256, default="")
    confirmed = models.BooleanField(default=False)

    class Meta:
        db_table = 'User'


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ":" + self.code

    class Meta:
        db_table = 'tb_confirmCode'
        ordering = ['-c_time']
        verbose_name = '确认码'
        verbose_name_plural = verbose_name


class Activities(models.Model):
    hosts = models.ForeignKey("User", on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    programs = models.CharField(max_length=256)
    t_id = models.IntegerField(default=0)  # 相应资源、问题的id
    s_id = models.IntegerField(default=0)  # 问题/资源对应的空间的id

    class Meta:
        db_table = 'Activities'


class Notices(models.Model):
    id = models.AutoField(primary_key=True)
    hosts = models.ForeignKey("User", on_delete=models.CASCADE, default="")
    notice_type = models.CharField(max_length=256, default="")
    notice_id = models.IntegerField(verbose_name="通知内容（评论等）的ID", default="")
    notice_title = models.CharField(max_length=256, default="")
    create_time = models.DateField(auto_now=True)

    class Meta:
        db_table = 'Notices'


class Collects(models.Model):
    id = models.AutoField(primary_key=True)
    hosts = models.ForeignKey("User", on_delete=models.CASCADE)
    collect_type = models.CharField(max_length=256)
    collect_id = models.IntegerField(verbose_name="通知内容（评论等）的ID")
    collect_title = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Collects'


class Follows(models.Model):
    id = models.AutoField(primary_key=True)
    following = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="关注者")
    # followed = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="被关注者")
    followed_type = models.CharField(max_length=50)
    followed_id = models.IntegerField(verbose_name="关注的人/学习空间id")
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Follows'


class Mails(models.Model):  # 私信
    id = models.AutoField(primary_key=True)
    texts = models.TextField()
    user1 = models.ForeignKey("User", on_delete=models.CASCADE)
    user2 = models.IntegerField()
    texts_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Mails'


class Likes(models.Model):
    id = models.AutoField(primary_key=True)
    hosts = models.ForeignKey("User", on_delete=models.CASCADE)
    liked_type = models.CharField(max_length=256)
    liked_id = models.IntegerField()
    liked_time = models.DateTimeField()

    class Meta:
        db_table = 'Likes'


class StudySpaces(models.Model):
    id = models.AutoField(primary_key=True)
    space_name = models.CharField(max_length=50)
    space_introduction = models.CharField(max_length=200)
    space_index = models.CharField(max_length=1000, default="")  # 主页内容
    space_picture = models.FileField(default="")  # 学习空间封面图片
    space_permission = models.IntegerField()  # 0为公开,非0为私有
    create_time = models.DateTimeField()
    last_update_time = models.DateTimeField()
    creator_id = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'StudySpaces'


class SpaceNotices(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)  # 从属的学习空间id
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)  # 创建者id
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    create_time = models.DateTimeField()
    last_update_time = models.DateTimeField()

    class Meta:
        db_table = 'Space_Notices'


class SpaceResources(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    resource_name = models.CharField(max_length=100)
    introduction = models.CharField(max_length=500)
    file = models.FileField()
    create_time = models.DateTimeField()
    last_update_time = models.DateTimeField()

    class Meta:
        db_table = 'Space_Resources'


class SpaceExercises(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.CharField(max_length=100)  # 题目
    type = models.CharField(max_length=100)  # 题目标题
    difficulty = models.CharField(max_length=10)  # 题目难度
    answer = models.CharField(max_length=100)
    create_time = models.DateTimeField()
    last_update_time = models.DateTimeField()

    class Meta:
        db_table = 'Space_Exercises'


class SpaceQuestions(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)
    create_time = models.DateTimeField()
    last_update_time = models.DateTimeField()

    class Meta:
        db_table = 'Space_Questions'


# 可以对学习空间中的习题、讨论问题、公告等基本所有内容进行评论
class SpaceComments(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    element_id = models.IntegerField()
    comment_type = models.IntegerField()  # 用数字代表评论的对象是学习空间中的哪个内容
    content = models.CharField(max_length=500)
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'Space_Comments'


class SpaceGroups(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)  # 群组创建者id
    group_name = models.CharField(max_length=50)
    members = models.ManyToManyField(to=User, related_name='Space_Groups_to_Users')
    create_time = models.DateTimeField()
    last_update_time = models.DateTimeField()

    class Meta:
        db_table = 'Space_Groups'


class SpaceLooks(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)  # 浏览空间id
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)  # 浏览者id
    watch_time = models.DateTimeField()

    class Meta:
        db_table = 'Space_looks'


class SpaceLikes(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)  # 点赞空间id
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)  # 点赞者id
    like_time = models.DateTimeField()

    class Meta:
        db_table = 'Space_likes'


class SpaceFollows(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)  # 空间id
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)  # 点赞者id
    follow_time = models.DateTimeField()

    class Meta:
        db_table = 'Space_follows'


class SpaceMembers(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)  # 空间id
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)  # 成员id
    is_admin = models.IntegerField()  # 0为普通成员,非0为管理者（空间创建者无需在此表添加）
    join_time = models.DateTimeField()  # 成为成员的时间

    class Meta:
        db_table = 'Space_members'

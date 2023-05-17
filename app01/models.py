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
    like = models.IntegerField(default=0, verbose_name="点赞数")
    tags = models.CharField(max_length=256, default="")
    confirmed = models.BooleanField(default=False)


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
    create_time = models.DateField(auto_now=True)
    programs = models.CharField(max_length=256)


class Notices(models.Model):
    hosts = models.ForeignKey("User", on_delete=models.CASCADE)
    notice_type = models.CharField(max_length=256)
    notice_id = models.IntegerField(verbose_name="通知内容（评论等）的ID")
    notice_title = models.CharField(max_length=256)
    create_time = models.DateField(auto_now=True)


class Collects(models.Model):
    hosts = models.ForeignKey("User", on_delete=models.CASCADE)
    collect_type = models.CharField(max_length=256)
    collect_id = models.IntegerField(verbose_name="通知内容（评论等）的ID")
    collect_title = models.CharField(max_length=256)
    create_time = models.DateField(auto_now=True)


class Follows(models.Model):
    following = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="关注者")
    # followed = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="被关注者")
    followed_type = models.CharField(max_length=50)
    followed_id = models.IntegerField(verbose_name="关注的人/学习空间id")
    create_time = models.DateField(auto_now=True)


class Mails(models.Model):
    texts = models.TextField()
    user1 = models.ForeignKey("User", on_delete=models.CASCADE)
    user2 = models.IntegerField()
    texts_time = models.DateField(auto_now=True)


class Likes(models.Model):
    hosts = models.ForeignKey("User", on_delete=models.CASCADE)
    like_type = models.CharField(max_length=256)
    liked_id = models.IntegerField()


class StudySpaces(models.Model):
    id = models.AutoField(primary_key=True)
    space_name = models.CharField(max_length=50)
    space_introduction = models.CharField(max_length=200)
    space_index = models.CharField(max_length=1000)  # 主页内容
    space_picture = models.BinaryField()  # 学习空间封面图片
    create_time = models.DateTimeField()
    creator_id = models.ForeignKey('User', on_delete=models.CASCADE)


class SpaceNotices(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)  # 从属的学习空间id
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)  # 创建者id
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    create_time = models.DateTimeField()


class SpaceResources(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100)
    file = models.BinaryField()
    create_time = models.DateTimeField()


class SpaceExercises(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.CharField(max_length=100)  # 题目
    type = models.CharField(max_length=10)  # 题目类型
    difficulty = models.CharField(max_length=10)  # 题目难度
    answer = models.CharField(max_length=100)
    create_time = models.DateTimeField()


class SpaceQuestions(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)
    create_time = models.DateTimeField()


# 可以对学习空间中的习题、讨论问题、公告等基本所有内容进行评论
class SpaceComments(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    comment_type = models.IntegerField()  # 用数字代表评论的对象是学习空间中的哪个内容
    content = models.CharField(max_length=500)
    create_time = models.DateTimeField()


class SpaceGroups(models.Model):
    id = models.AutoField(primary_key=True)
    space_id = models.ForeignKey('StudySpaces', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)  # 群组创建者id
    group_name = models.CharField(max_length=50)
    members = models.ManyToManyField(to=User, related_name='SpaceGroups_Users')

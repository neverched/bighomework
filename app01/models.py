from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)


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





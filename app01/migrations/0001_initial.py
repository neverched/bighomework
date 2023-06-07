# Generated by Django 4.1.7 on 2023-06-07 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(default='', max_length=256)),
                ('gender', models.IntegerField(default=0)),
                ('intro', models.CharField(default='', max_length=256)),
                ('organization', models.CharField(default='', max_length=50, verbose_name='所属组织')),
                ('destination', models.CharField(default='', max_length=256)),
                ('job', models.CharField(default='', max_length=256)),
                ('followers', models.IntegerField(default=0, verbose_name='粉丝数')),
                ('followings', models.IntegerField(default=0, verbose_name='关注数')),
                ('like', models.IntegerField(default=0, verbose_name='点赞数')),
                ('tags', models.CharField(default='', max_length=256)),
                ('confirmed', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='StudySpaces',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('space_name', models.CharField(max_length=50)),
                ('space_introduction', models.CharField(max_length=200)),
                ('space_index', models.CharField(default='', max_length=1000)),
                ('space_picture', models.FileField(default='', upload_to='')),
                ('space_permission', models.IntegerField()),
                ('create_time', models.DateTimeField()),
                ('last_update_time', models.DateTimeField()),
                ('creator_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'StudySpaces',
            },
        ),
        migrations.CreateModel(
            name='SpaceResources',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('resource_name', models.CharField(max_length=100)),
                ('introduction', models.CharField(max_length=500)),
                ('file', models.FileField(upload_to='')),
                ('create_time', models.DateTimeField()),
                ('last_update_time', models.DateTimeField()),
                ('space_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.studyspaces')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'Space_Resources',
            },
        ),
        migrations.CreateModel(
            name='SpaceQuestions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=1000)),
                ('create_time', models.DateTimeField()),
                ('last_update_time', models.DateTimeField()),
                ('space_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.studyspaces')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'Space_Questions',
            },
        ),
        migrations.CreateModel(
            name='SpaceNotices',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=500)),
                ('create_time', models.DateTimeField()),
                ('last_update_time', models.DateTimeField()),
                ('space_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.studyspaces')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'Space_Notices',
            },
        ),
        migrations.CreateModel(
            name='SpaceMembers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_admin', models.IntegerField()),
                ('join_time', models.DateTimeField()),
                ('space_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.studyspaces')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'Space_members',
            },
        ),
        migrations.CreateModel(
            name='SpaceLooks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('watch_time', models.DateTimeField()),
                ('space_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.studyspaces')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'Space_looks',
            },
        ),
        migrations.CreateModel(
            name='SpaceLikes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('like_time', models.DateTimeField()),
                ('space_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.studyspaces')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'Space_likes',
            },
        ),
        migrations.CreateModel(
            name='SpaceGroups',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('group_name', models.CharField(max_length=50)),
                ('create_time', models.DateTimeField()),
                ('last_update_time', models.DateTimeField()),
                ('members', models.ManyToManyField(related_name='Space_Groups_to_Users', to='app01.user')),
                ('space_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.studyspaces')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'Space_Groups',
            },
        ),
        migrations.CreateModel(
            name='SpaceFollows',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('follow_time', models.DateTimeField()),
                ('space_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.studyspaces')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'Space_follows',
            },
        ),
        migrations.CreateModel(
            name='SpaceExercises',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('difficulty', models.CharField(max_length=10)),
                ('answer', models.CharField(max_length=100)),
                ('create_time', models.DateTimeField()),
                ('last_update_time', models.DateTimeField()),
                ('space_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.studyspaces')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'Space_Exercises',
            },
        ),
        migrations.CreateModel(
            name='SpaceComments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('element_id', models.IntegerField()),
                ('comment_type', models.IntegerField()),
                ('content', models.CharField(max_length=500)),
                ('create_time', models.DateTimeField()),
                ('space_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.studyspaces')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'Space_Comments',
            },
        ),
        migrations.CreateModel(
            name='Notices',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('notice_type', models.CharField(default='', max_length=256)),
                ('notice_id', models.IntegerField(default='', verbose_name='通知内容（评论等）的ID')),
                ('notice_title', models.CharField(default='', max_length=256)),
                ('create_time', models.DateField(auto_now=True)),
                ('hosts', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'Notices',
            },
        ),
        migrations.CreateModel(
            name='Mails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('texts', models.TextField()),
                ('user2', models.IntegerField()),
                ('texts_time', models.DateTimeField(auto_now=True)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'Mails',
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('liked_type', models.CharField(max_length=256)),
                ('liked_id', models.IntegerField()),
                ('liked_time', models.DateTimeField()),
                ('hosts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'Likes',
            },
        ),
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('followed_type', models.CharField(max_length=50)),
                ('followed_id', models.IntegerField(verbose_name='关注的人/学习空间id')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user', verbose_name='关注者')),
            ],
            options={
                'db_table': 'Follows',
            },
        ),
        migrations.CreateModel(
            name='ConfirmString',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'verbose_name': '确认码',
                'verbose_name_plural': '确认码',
                'db_table': 'tb_confirmCode',
                'ordering': ['-c_time'],
            },
        ),
        migrations.CreateModel(
            name='Collects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('collect_type', models.CharField(max_length=256)),
                ('collect_id', models.IntegerField(verbose_name='通知内容（评论等）的ID')),
                ('collect_title', models.CharField(max_length=256)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('hosts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'Collects',
            },
        ),
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('programs', models.CharField(max_length=256)),
                ('t_id', models.IntegerField(default=0)),
                ('s_id', models.IntegerField(default=0)),
                ('hosts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user')),
            ],
            options={
                'db_table': 'Activities',
            },
        ),
    ]

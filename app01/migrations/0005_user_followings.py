# Generated by Django 4.1 on 2023-05-21 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0004_user_confirmed_confirmstring"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="followings",
            field=models.IntegerField(default=0, verbose_name="关注数"),
        ),
    ]

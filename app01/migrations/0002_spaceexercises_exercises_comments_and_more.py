# Generated by Django 4.1 on 2023-05-29 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="spaceexercises",
            name="exercises_comments",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="spaceexercises",
            name="exercises_likes",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="spacenotices",
            name="space_follows",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="spacenotices",
            name="space_likes",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="spacequestions",
            name="questions_comments",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="spacequestions",
            name="questions_likes",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="spaceresources",
            name="resources_comments",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="spaceresources",
            name="resources_likes",
            field=models.IntegerField(default=0),
        ),
    ]

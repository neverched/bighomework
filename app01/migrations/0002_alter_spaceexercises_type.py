# Generated by Django 4.1.7 on 2023-06-07 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spaceexercises',
            name='type',
            field=models.CharField(max_length=100),
        ),
    ]

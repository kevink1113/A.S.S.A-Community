# Generated by Django 3.1.5 on 2021-02-09 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20210201_1909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='dislike',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='like',
        ),
    ]

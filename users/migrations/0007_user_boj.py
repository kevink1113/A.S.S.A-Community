# Generated by Django 3.1.5 on 2021-01-23 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_auto_20210123_2348"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="boj",
            field=models.URLField(blank=True, null=True),
        ),
    ]

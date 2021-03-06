# Generated by Django 3.1.5 on 2021-01-23 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_soldier",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="mil_fin",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="mil_start",
            field=models.DateField(blank=True, null=True),
        ),
    ]

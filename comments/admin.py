from django.contrib import admin
from . import models


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    """ Comment Admin Definition """

    list_filter = ("user",)

    list_display = ("__str__", "post", "user", "like_sum")

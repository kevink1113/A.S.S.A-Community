from django.contrib import admin
from . import models


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    """ Comment Admin Definition """

    list_display = ("__str__", "like_sum")

from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    """ Post Admin Definition """

    list_display = ("__str__", "like_sum")

from django.db import models
from django.db.models import Count
from core import models as core_models
from django.urls import reverse
from comments import models as comment_models


class Post(core_models.TimeStampModel):
    """ Review Model Definition """

    title = models.CharField(max_length=30)
    content = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="user_post", on_delete=models.CASCADE
    )
    # like = models.PositiveIntegerField(default=0)
    # dislike = models.PositiveIntegerField(default=0)

    like_users = models.ManyToManyField("users.User", related_name='like_posts', blank=True)
    dislike_users = models.ManyToManyField("users.User", related_name='dislike_posts', blank=True)

    def __str__(self):
        return f"{self.title} - {self.user}"

    def like_sum(self):
        return self.like_users.count() - self.dislike_users.count()
        # return self.like - self.dislike

from django.db import models
from core import models as core_models


class Comment(core_models.TimeStampModel):
    """ Review Model Definition """

    content = models.TextField()
    post = models.ForeignKey(
        "posts.Post", related_name="posts", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "users.User", related_name="user", on_delete=models.CASCADE
    )
    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.created}"

    def like_sum(self):
        return self.like - self.dislike

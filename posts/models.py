from django.db import models
from core import models as core_models


class Post(core_models.TimeStampModel):
    """ Review Model Definition """

    title = models.TextField()
    content = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.user}"

    def like_sum(self):
        return self.like - self.dislike

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # followers
    followers = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="following"
    )


# Posts
class Post(models.Model):
    # Poster
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    # Post content,
    content = models.TextField(max_length=1000, blank=False)
    # posted time
    timestamp = models.DateTimeField(auto_now_add=True)
    # likes
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.content} by {self.user}"

    def liked(self, user):
        if self.likes.filter(username=user.username):
            return True
        else:
            return False

    def like_count(self):
        like_count = self.likes.count()
        if like_count > 1:
            return f"{like_count} Likes"
        elif like_count == 1:
            return f"{like_count} Like"
        else:
            return f"Like"

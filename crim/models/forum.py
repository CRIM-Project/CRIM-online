from django.db import models
from django.urls import reverse

from .group import CRIMGroup
from .user import CRIMUserProfile


class ForumPost(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    # Reference to the user who created the post.
    user = models.ForeignKey(
        CRIMUserProfile, null=True, blank=True, on_delete=models.SET_NULL
    )
    # Reference to the group to which the post belongs.
    group = models.ForeignKey(
        CRIMGroup, null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("view_forum_post", args=[self.pk])

    def __str__(self):
        if self.user:
            return "{0.title} (by {0.user})".format(self)
        else:
            return self.title


class ForumComment(models.Model):
    text = models.TextField()
    # Reference to the user who created the comment.
    user = models.ForeignKey(CRIMUserProfile, null=True, on_delete=models.SET_NULL)
    # The parent of the comment, which may be null if the comment is at the top-level.
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    # The post to which the comment belongs.
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return self.post.get_absolute_url()

    def __str__(self):
        if self.user:
            return 'Comment on "{0.post.title}" by {0.user}'.format(self)
        else:
            return 'Comment on "{0.post.title}"'.format(self)

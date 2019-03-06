from django.db import models

from .group import CRIMGroup
from .user import CRIMUserProfile


class ForumPost(models.Model):
    text = models.TextField()
    # Reference to the user who created the post.
    user = models.ForeignKey(CRIMUserProfile, null=True, on_delete=models.SET_NULL)
    # Reference to the group to which the post belongs.
    group = models.ForeignKey(CRIMGroup, null=True, on_delete=models.SET_NULL)


class ForumComment(models.Model):
    text = models.TextField()
    # Reference to the user who created the comment.
    user = models.ForeignKey(CRIMUserProfile, null=True, on_delete=models.SET_NULL)
    # The parent of the comment, which may be null if the comment is at the top-level.
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    # The post to which the comment belongs.
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)

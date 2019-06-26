from django.db import models
from django.urls import reverse
from django.utils import timezone

from .group import CRIMGroup


class CRIMForumPost(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Forum post'
        verbose_name_plural = 'Forum posts'
        ordering = ['-created_at']
        unique_together = [('created_at', 'author')]

    post_id = models.CharField(
        'Post ID',
        max_length=64,
        # We have to allow blank `post_id` because of the intermediate period
        # between the item's initial creation and its receiving of the id
        # based on author and timestamp.
        blank=True,
    )

    # The parent of the comment, which may be null if the post is at the top-level.
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
    )
    head = models.ForeignKey(
        'self',
        null=True,
        on_delete=models.CASCADE,
        related_name='all_replies',
    )

    # Titles should generally be blank iff the post is not at the top level.
    title = models.CharField(max_length=128, blank=True)
    text = models.TextField()
    # Reference to the user who created_at the post.
    author = models.ForeignKey(
        'CRIMUserProfile',
        null=True,
        on_delete=models.SET_NULL,
        related_name='forum_posts',
    )
    # Reference to the group to which the post belongs.
    group = models.ForeignKey(
        CRIMGroup, null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    edited = models.BooleanField(default=False)
    # When a comment has been deleted, the object is kept, but the text is wiped
    # out and `alive` is set to False. This field is used to prevent the object
    # from being included in lists, and to prevent the user from changing the
    # text again.
    alive = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('forum-view-post', args=[self.post_id])

    def __str__(self):
        if not self.head:
            return "{0.author.name}: “{0.title}”".format(self)
        else:
            return "Reply by {} on “{}” - {}".format(
                self.author.name,
                self.head.title,
                self.created_at.strftime('%Y-%m-%d at %H:%M'),
            )

    def _get_unique_slug(self):
        slug_base = self.author.user.username + '/' + self.created_at.strftime('%Y-%m-%dT%H:%M:%S')
        unique_slug = slug_base
        num = 1
        while CRIMForumPost.objects.filter(post_id=unique_slug).exists():
            unique_slug = '{}.{}'.format(slug_base, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        # Set the timestamps
        if not self.post_id:
            self.created_at = timezone.now()
            self.post_id = self._get_unique_slug()
        self.updated_at = timezone.now()

        # Set the head to be the same as the parent's head; if there is no
        # parent, then there is no head either.
        if self.parent:
            self.head = self.parent.head if self.parent.head else self.parent
        else:
            self.head = None

        # Then save
        super().save(*args, **kwargs)

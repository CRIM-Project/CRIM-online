from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CRIMComment(models.Model):
    class Meta:
        app_label = "crim"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    author = models.ForeignKey(
        'CRIMUserProfile',
        models.CASCADE,
        related_name='comments',
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=16)
    content_object = GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    text = models.TextField()

    def __unicode__(self):
        return '{0} ({1} {2})'.format(self.piece, self.author, self.created)

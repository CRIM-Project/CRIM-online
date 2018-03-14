from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CRIMDiscussion(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Discussion'
        verbose_name_plural = 'Discussions'

    author = models.ForeignKey(
        'CRIMUserProfile',
        on_delete=models.SET_NULL,
        null=True,
        related_name='discussions',
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    text = models.TextField()

    def __unicode__(self):
        return '{0} ({1} {2})'.format(self.piece, self.author, self.created)

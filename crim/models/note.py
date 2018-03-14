from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CRIMNote(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

    author = models.ForeignKey(
        'CRIMUserProfile',
        on_delete=models.CASCADE,
        related_name='notes',
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    text = models.TextField()

    def __unicode__(self):
        return '{0} ({1} {2})'.format(self.piece, self.author, self.created)

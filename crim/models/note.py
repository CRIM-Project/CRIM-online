from django.db import models


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

    def str(self):
        return '{0} ({1} {2})'.format(self.piece, self.author, self.created)

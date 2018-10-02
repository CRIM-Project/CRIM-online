from django.db import models


class CRIMComment(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        unique_together = ('author', 'created')

    comment_id = models.CharField(max_length=64, blank=True)

    author = models.ForeignKey(
        'CRIMUserProfile',
        on_delete=models.CASCADE,
        related_name='comments',
    )

    piece = models.ForeignKey(
        'CRIMPiece',
        on_delete=models.SET_NULL,
        to_field='piece_id',
        blank=True,
        null=True,
        related_name='comments_as_piece',
    )

    # Allow comments to be added to masses, treatises, sources,
    # people, observations, relationships, and genres as well...
    # Probably best done with a generic foreign key
    # <https://docs.djangoproject.com/en/2.1/ref/contrib/contenttypes/#generic-relations>

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    # When a comment has been deleted, the object is kept, but the text is wiped
    # out and `alive` is set to False. This field is used to prevent the object
    # from being included in lists, and to prevent the user from changing the
    # text again.
    alive = models.BooleanField(default=True)

    text = models.TextField()

    def _get_unique_slug(self):
        slug_base = self.author.user.username + '/' + self.created.strftime('%Y-%m-%dT%H:%M:%S')
        unique_slug = slug_base
        num = 1
        while CRIMComment.objects.filter(comment_id=unique_slug).exists():
            unique_slug = '{}.{}'.format(slug_base, num)
            num += 1
        return unique_slug

    def __str__(self):
        return '{0} on [{1}] at {2}'.format(self.author, self.piece.piece_id, self.created.strftime('%Y-%m-%d %H:%M:%S'))

    def save(self):
        # Need to save once to get the `created` field filled
        super().save()
        # Then use that date and time to fill in the id
        if not self.comment_id:
            self.comment_id = self._get_unique_slug()
        # And save again
        super().save()

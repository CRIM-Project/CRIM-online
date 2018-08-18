from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from crim.models.user import CRIMUserProfile


class CRIMFavorite(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'

    user = models.ForeignKey(
        CRIMUserProfile,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='favorites',
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=32)
    content_object = GenericForeignKey('content_type', 'object_id')

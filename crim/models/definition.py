from django.db import models
from django.db.models import JSONField

class CRIMDefinition(models.Model):
    class Meta:
        app_label = 'crim'
        verbose_name = 'Definition'
        verbose_name_plural = 'Definitions'

    observation_definition = JSONField(null=True)
    relationship_definition = JSONField(null=True)

    remarks = models.TextField('remarks (supports Markdown)', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)

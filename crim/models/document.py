from django.db import models


class CRIMDocument(models.Model):
    class Meta:
        app_label = "crim"
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    id = models.CharField(max_length=16, unique=True, db_index=True)
    title = models.CharField(max_length=64, blank=True)
    contents = models.ManyToManyField(to=CRIMDocument)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return u"{0}: {1}".format(self.id, self.title)


class CRIMTreatise(CRIMDocument):
    class Meta:
        app_label = "crim"
        verbose_name = "Treatise"
        verbose_name_plural = "Treatises"


class CRIMSource(CRIMDocument):
    class Meta:
        app_label = "crim"
        verbose_name = "Source"
        verbose_name_plural = "Sources"

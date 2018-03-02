from django.db import models


class CRIMPiece(CRIMDocument):
    class Meta:
        app_label = "crim"
        verbose_name = "Piece"
        verbose_name_plural = "Pieces"

    id = models.CharField(max_length=16, unique=True, db_index=True)
    title = models.CharField(max_length=64, blank=True, db_index=True)
#     composer_id = models.ForeignKey(CRIMPerson, to='id', db_index=True)
#     forces = models.CharField(max_length=16, blank=True)
    pdf_link = models.CharField(max_length=255, blank=True)
    mei_link = models.CharField(max_length=255, blank=True)
#     audio_link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return u"{0}: {1}".format(self.id, self.title)

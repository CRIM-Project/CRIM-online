from django.db import models

from crim.models.document import CRIMDocument
# from crim.models.person import CRIMPerson


class CRIMMass(CRIMDocument):
    class Meta:
        app_label = "crim"
        verbose_name = "Mass"
        verbose_name_plural = "Masses"
    
    # Note that we do not need to list mass movements as
    # "Contents" of a mass: mass movements already reference
    # the mass model specially.

#     composer_id = models.ForeignKey(CRIMPerson, to='id', db_index=True)

    def __str__(self):
        return u"{0}: {1}".format(self.id, self.title)

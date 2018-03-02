from django.db import models
from django.contrib.auth.models import User

from crim.models.person import CRIMPerson
from crim.models.mass import CRIMMass
from crim.models.piece import CRIMPiece
from crim.models.comment import CRIMComment
from crim.models.discussion import CRIMDiscussion


class CRIMUserProfile(models.Model):
    class Meta:
        app_label = "duchemin"

    user = models.OneToOneField(User, db_index=True)
    favorite_masses = models.ManyToManyField(CRIMMass, blank=True)
    favorite_pieces = models.ManyToManyField(CRIMPiece, blank=True)
    favorite_documents = models.ManyToManyField(CRIMDocument, blank=True)
    favorite_comments = models.ManyToManyField(CRIMComment, blank=True)
    favorite_discussions = models.ManyToManyField(CRIMDiscussion, blank=True)
#     project_role = models.CharField(max_length=64, blank=True, null=True)
    person = models.ForeignKey(CRIMPerson,
                               blank=True,
                               null=True,
                               db_index=True,
                               help_text="Link this account with a CRIM User",
                               related_name="profile"
    )

    def __str__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)

User.profile = property(lambda u: CRIMUserProfile.objects.get_or_create(user=u)[0])

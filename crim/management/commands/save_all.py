from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from crim.models.definition import CRIMDefinition
from crim.models.document import CRIMTreatise, CRIMSource
from crim.models.mass import CRIMMass
from crim.models.observation import CRIMObservation, CJObservation
from crim.models.person import CRIMPerson
from crim.models.piece import CRIMPiece
from crim.models.relationship import CRIMRelationship, CJRelationship
from crim.models.role import CRIMRole
from crim.models.user import CRIMUserProfile


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for person in CRIMPerson.objects.all():
            person.save()
        for role in CRIMRole.objects.all():
            role.save()

        for treatise in CRIMTreatise.objects.all():
            treatise.save()
        for source in CRIMSource.object.all():
            source.save()

        for piece in CRIMPiece.objects.all():
            piece.save()
        for mass in CRIMMass.objects.all():
            mass.save()

        # These next two are the old types which are deprecated
        for observation in CRIMObservation.objects.all():
            observation.save()
        for relationship in CRIMRelationship.objects.all():
            relationship.save()

        for definition in CRIMDefinition.objects.all():
            definition.save()
        for observation in CJObservation.objects.all():
            observation.save()
        for relationship in CJRelationship.objects.all():
            relationship.save()

        for user in User.objects.all():
            user.save()
        for profile in CRIMUserProfile.objects.all():
            profile.save()

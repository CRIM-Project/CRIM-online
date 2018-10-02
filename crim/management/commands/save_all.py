from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from crim.models.observation import CRIMObservation
from crim.models.person import CRIMPerson
from crim.models.relationship import CRIMRelationship
from crim.models.role import CRIMRole
from crim.models.user import CRIMUserProfile


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for person in CRIMPerson.objects.all():
            person.save()
        for role in CRIMRole.objects.all():
            role.save()

        for observation in CRIMObservation.objects.all():
            observation.save()
        for relationship in CRIMRelationship.objects.all():
            relationship.save()

        for user in User.all():
            user.save()
        for profile in CRIMUserProfile.objects.all():
            profile.save()

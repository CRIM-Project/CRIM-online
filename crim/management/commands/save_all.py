from django.core.management.base import BaseCommand
from crim.models.person import CRIMPerson
from crim.models.role import CRIMRole


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for person in CRIMPerson.objects.all():
            person.save()
        for role in CRIMRole.objects.all():
            role.save()
        # TODO: add all other fields

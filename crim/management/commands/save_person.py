from django.core.management.base import BaseCommand
from crim.models.person import CRIMPerson


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for person in CRIMPerson.objects.all():
            person.save()

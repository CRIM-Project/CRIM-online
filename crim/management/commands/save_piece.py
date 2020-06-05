from django.core.management.base import BaseCommand
from crim.models.piece import CRIMPiece


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for person in CRIMPiece.objects.all():
            person.save()

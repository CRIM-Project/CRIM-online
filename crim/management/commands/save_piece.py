from django.core.management.base import BaseCommand
from crim.models.piece import CRIMPiece


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for piece in CRIMPiece.objects.all():
            piece.save()

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from crim.models.piece import CRIMPiece


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for piece in CRIMPiece.objects.all():
            piece.mei_links = piece.mei_links.replace('https://crimproject.org', 'http://127.0.0.1:8000/static')
            piece.pdf_links = piece.pdf_links.replace('https://crimproject.org', 'http://127.0.0.1:8000/static')
            piece.save()

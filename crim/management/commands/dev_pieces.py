from django.core.management.base import BaseCommand

from crim.models.piece import CRIMPiece
from crim.views.piece import render_piece


class Command(BaseCommand):
    help = 'Changes the MEI links of every piece to include "dev".'

    def handle(self, *args, **options):
        for piece in CRIMPiece.objects.all():
            print('Altering {}'.format(piece.piece_id))
            piece.mei_links = piece.mei_links.replace(
                    "https://crimproject.org",
                    "https://dev.crimproject.org",
                )
            piece.save()

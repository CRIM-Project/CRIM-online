from django.core.management.base import BaseCommand

from crim.models.piece import CRIMPiece
from crim.views.piece import render_piece


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for piece in CRIMPiece.objects.all():
            print('Caching {}'.format(piece.piece_id))
            for i in range(30):
                render_piece(piece.piece_id, i+1)

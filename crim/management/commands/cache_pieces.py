from django.core.management.base import BaseCommand

from crim.models.piece import CRIMPiece
from crim.views.piece import render_piece


class Command(BaseCommand):
    help = 'Re-caches the score of a given piece, or all pieces if none is given.'

    def add_arguments(self, parser):
        parser.add_argument('piece_ids', nargs='*')

    def handle(self, *args, **options):
        if not options['piece_ids']:
            for piece in CRIMPiece.objects.all():
                print('Caching {}'.format(piece.piece_id))
                for i in range(30):
                    render_piece(piece.piece_id, i+1)
        else:
            for piece_id in options['piece_ids']:
                try:
                    piece = CRIMPiece.objects.get(piece_id=piece_id)
                    print('Caching {}'.format(piece.piece_id))
                    for i in range(30):
                        render_piece(piece.piece_id, i+1)
                except CRIMPiece.DoesNotExist:
                    raise CommandError('Piece "%s" does not exist' % piece_id)

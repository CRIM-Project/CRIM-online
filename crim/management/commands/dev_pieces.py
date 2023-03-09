from django.core.management.base import BaseCommand

from crim.models.piece import CRIMPiece


class Command(BaseCommand):
    help = 'Changes the MEI links of every piece to include "dev".'

    def handle(self, *args, **options):
        for piece in CRIMPiece.objects.all():
            print(piece.piece_id, end='')
            if "https://crimproject.org" in piece.mei_links:
                print(' - altered')
            else:
                print()
            piece.mei_links = piece.mei_links.replace(
                    "https://crimproject.org",
                    "https://dev.crimproject.org",
                )
            piece.save()

from django.core.management.base import BaseCommand

from crim.models.observation import CRIMObservation
from crim.views.observation import render_observation


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for observation in CRIMObservation.objects.all():
            print('Caching first highlighted page of <{}>'.format(observation.id))
            render_observation(
                    observation.id,
                    observation.piece.piece_id,
                    observation.ema,
                    None,
                )
        for observation in CRIMObservation.objects.all():
            print('Caching all pages of <{}>'.format(observation.id))
            for i in range(35):
                render_observation(
                        observation.id,
                        observation.piece.piece_id,
                        observation.ema,
                        i+1,
                    )

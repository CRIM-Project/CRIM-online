from django.core.management.base import BaseCommand

from crim.models.observation import CRIMObservation
from crim.views.observation import render_observation


class Command(BaseCommand):
    help = 'Caches 35 pages of a single observation.'

    def add_arguments(self, parser):
        parser.add_argument('observation_ids', nargs='+', type=int)

    def handle(self, *args, **kwargs):
        for observation_id in kwargs['observation_ids']:
            observation = CRIMObservation.objects.get(id=observation_id)
            print('Caching first highlighted page of <{}>'.format(observation_id))
            try:
                render_observation(
                        observation.id,
                        observation.piece.piece_id,
                        observation.ema,
                        None,
                    )
            except:
                print('ERROR caching first highlighted page of <{}>'.format(observation.id))
        for observation_id in kwargs['observation_ids']:
            observation = CRIMObservation.objects.get(id=observation_id)
            print('Caching all pages of <{}>'.format(observation_id))
            try:
                for i in range(30):
                    render_observation(
                            observation.id,
                            observation.piece.piece_id,
                            observation.ema,
                            i+1,
                        )
            except:
                print('ERROR caching all pages of <{}>'.format(observation.id))

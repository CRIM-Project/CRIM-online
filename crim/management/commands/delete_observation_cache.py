from django.core.cache import caches
from django.core.management.base import BaseCommand

from crim.models.observation import CRIMObservation
from crim.views.observation import render_observation


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('observation_ids', nargs='+', type=int)

    def handle(self, *args, **kwargs):
        for observation_id in kwargs['observation_ids']:
            try:
                caches['observations'].delete('{},'.format(observation_id))
            except:
                print("not cached")
            for i in range(30):
                try:
                    caches['observations'].delete('{},{}'.format(observation_id, i+1))
                except:
                    print('page not cached')

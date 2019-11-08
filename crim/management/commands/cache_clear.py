from django.core.cache import caches
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        caches['pieces'].clear()
        caches['observations'].clear()

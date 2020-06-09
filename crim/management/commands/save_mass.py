from django.core.management.base import BaseCommand
from crim.models.mass import CRIMMass


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for mass in CRIMMass.objects.all():
            mass.save()

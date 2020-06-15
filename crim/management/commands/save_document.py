from django.core.management.base import BaseCommand
from crim.models.document import CRIMTreatise, CRIMSource


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for treatise in CRIMTreatise.objects.all():
            treatise.save()
        for source in CRIMSource.objects.all():
            source.save()

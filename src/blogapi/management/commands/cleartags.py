from django.core.management.base import BaseCommand
from taggit.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        Tag.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Ended without errors"))

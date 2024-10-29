from django.core.management.base import BaseCommand
from taggit.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        Tag.objects.all().delete()

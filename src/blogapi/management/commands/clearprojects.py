from django.core.management.base import BaseCommand

from ...models import Project


class Command(BaseCommand):
    def handle(self, *args, **options):
        Project.objects.all().delete()

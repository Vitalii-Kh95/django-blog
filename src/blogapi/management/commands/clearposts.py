from ...models import BlogPost
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        BlogPost.objects.all().delete()

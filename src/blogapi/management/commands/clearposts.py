from ...models import BlogPost
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        posts = BlogPost.objects.all()
        for post in posts:
            post.delete(remove_related_image=True)
        self.stdout.write(self.style.SUCCESS("Ended without errors"))

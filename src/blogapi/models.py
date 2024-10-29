from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        get_user_model(),
        related_name="%(class)ss",
        related_query_name="%(class)s",
        on_delete=models.CASCADE,
    )
    tags = TaggableManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogPost(Post):
    pass


class Project(Post):
    pass

from django.contrib.auth.models import User
from rest_framework import serializers
from taggit.serializers import TaggitSerializer

from .models import BlogPost, Project


class TagSerializer(serializers.Serializer):
    name = serializers.CharField()
    slug = serializers.SlugField()


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
    )

    class Meta:
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "content",
            "image",
            "created_at",
            "author",
            "tags",
        )

    def __str__(self) -> str:
        return f"{self.title}, {self.description}"


class BlogPostSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        model = BlogPost


class ProjectSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        model = Project

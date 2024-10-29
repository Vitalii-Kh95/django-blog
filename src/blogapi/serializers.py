from django.contrib.auth.models import User
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from .models import BlogPost, Project


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
    )

    def __str__(self) -> str:
        return f"{self.title}, {self.description}"


class BlogPostSerializer(PostSerializer):
    class Meta:
        model = BlogPost
        fields = "__all__"


class ProjectSerializer(PostSerializer):
    class Meta:
        model = Project
        fields = "__all__"

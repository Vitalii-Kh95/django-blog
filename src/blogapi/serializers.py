from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit.serializers import TaggitSerializer

from .models import BlogPost, Project


class TagSerializer(serializers.Serializer):
    name = serializers.CharField()
    slug = serializers.SlugField()


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    User = get_user_model()
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


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]  # adjust as needed


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm", None)
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data, password=password)
        return user

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag

from .models import BlogPost, Project
from .serializers import BlogPostSerializer, ProjectSerializer, TagSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = "slug"


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = "slug"


class TagListView(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        return Response(TagSerializer(tags, many=True).data)


class TagDetailView(APIView):
    def get(self, request, tag_slug):
        tag = Tag.objects.get(slug=tag_slug)

        qs1 = BlogPost.objects.filter(tags=tag)
        qs2 = Project.objects.filter(tags=tag)
        return Response(
            BlogPostSerializer(qs1, many=True, context={"request": request}).data
            + ProjectSerializer(qs2, many=True, context={"request": request}).data
        )

from rest_framework import filters, pagination, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag

from blogapi.models import BlogPost, Project
from blogapi.serializers import BlogPostSerializer, ProjectSerializer, TagSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing blog posts.
    """

    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description", "content"]
    pagination_class = pagination.LimitOffsetPagination
    ordering = ["-created_at"]
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        """
        List all blog posts, with optional filtering by tag.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())

            if request.GET.get("tag"):
                queryset = queryset.filter(tags__slug=request.GET.get("tag"))

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BlogPostViewSet(PostViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


class ProjectViewSet(PostViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TagListView(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        return Response(TagSerializer(tags, many=True).data)

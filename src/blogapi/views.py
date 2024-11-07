from rest_framework import filters, pagination, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag

from .models import BlogPost, Project
from .serializers import BlogPostSerializer, ProjectSerializer, TagSerializer


class PostViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description", "content"]
    pagination_class = pagination.LimitOffsetPagination
    ordering = ["-created_at"]
    lookup_field = "slug"

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.GET.get("tag"):
            queryset = queryset.filter(tags__slug=request.GET.get("tag"))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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


# class TagDetailView(APIView):
#     pagination_class = pagination.LimitOffsetPagination

#     def get(self, request, tag_slug):
#         tag = Tag.objects.get(slug=tag_slug)

#         qs1 = BlogPost.objects.filter(tags=tag)
#         qs2 = Project.objects.filter(tags=tag)
#         return Response(
#             {
#                 "posts": BlogPostSerializer(
#                     qs1, many=True, context={"request": request}
#                 ).data
#             }
#             | {
#                 "projects": ProjectSerializer(
#                     qs2, many=True, context={"request": request}
#                 ).data
#             }
#         )

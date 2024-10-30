from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BlogPostViewSet, ProjectViewSet, TagDetailView, TagListView

post_router = DefaultRouter()
post_router.register("posts", BlogPostViewSet, basename="posts")

project_router = DefaultRouter()
project_router.register("projects", ProjectViewSet, basename="projects")

app_name = "blogapi"
urlpatterns = [
    path("", include(post_router.urls)),
    path("", include(project_router.urls)),
    path("tags/", TagListView.as_view()),
    path("tags/<slug:tag_slug>/", TagDetailView.as_view()),
]

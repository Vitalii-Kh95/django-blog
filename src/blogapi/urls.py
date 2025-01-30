from django.urls import path, re_path

from blogapi.views.post_views import BlogPostViewSet, ProjectViewSet, TagListView
from blogapi.views.service_views import (
    HealthCheckView,
    api_root,
    catch_all_404_view,
    csrf_token_view,
)
from blogapi.views.user_views import (
    LoginView,
    RegistrationView,
    logout_view,
    whoami_view,
)

app_name = "blogapi"

urlpatterns = [
    path("", api_root, name="api-root"),
    # BlogPostViewSet Endpoints
    path(
        "posts/",
        BlogPostViewSet.as_view({"get": "list", "post": "create"}),
        name="posts-list",
    ),
    path(
        "posts/<slug:slug>/",
        BlogPostViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="posts-detail",
    ),
    # ProjectViewSet Endpoints
    path(
        "projects/",
        ProjectViewSet.as_view({"get": "list", "post": "create"}),
        name="projects-list",
    ),
    path(
        "projects/<slug:slug>/",
        ProjectViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="projects-detail",
    ),
    # Additional Endpoints
    path("tags/", TagListView.as_view(), name="tags-list"),
    path("csrf_token/", csrf_token_view, name="csrf-token"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("whoami/", whoami_view, name="whoami"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("health/", HealthCheckView.as_view(), name="health-check"),
    re_path(r"^.*$", catch_all_404_view, name="catch-all-404"),
]

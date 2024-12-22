from django.contrib.auth import authenticate, get_user_model, login, logout
from django.middleware.csrf import get_token
from rest_framework import filters, generics, pagination, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag

from .models import BlogPost, Project
from .permissions import IsAnonymous
from .serializers import (
    BlogPostSerializer,
    ProjectSerializer,
    RegistrationSerializer,
    TagSerializer,
)
from .utils import is_email


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


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_view(request):
    User = get_user_model()
    username_or_email = request.data.get(
        "username"
    )  # Use 'username' for consistency in the payload
    password = request.data.get("password")

    # Specific error messages for missing fields
    if not username_or_email and not password:
        return Response(
            {
                "username": ["This field is required."],
                "password": ["This field is required."],
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif not username_or_email:
        return Response(
            {"username": ["This field is required."]},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif not password:
        return Response(
            {"password": ["This field is required."]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if the input is an email or username
    try:
        if is_email(username_or_email):
            # Try to find the user by email
            user = User.objects.get(email=username_or_email)
            username = user.username  # Extract username for authentication
        else:
            username = username_or_email
    except User.DoesNotExist:
        return Response(
            {"username": ["Invalid username or email."]},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # Authenticate user
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response(
            {"username": user.username, "message": "Login successful"},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"password": ["Invalid credentials."]},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        logout(request)
        return Response(
            {"message": "Logout successful"}, status=status.HTTP_204_NO_CONTENT
        )
    except Exception as e:
        # Log the error for debugging
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Logout error: {e}")
        return Response(
            {"error": "Unexpected error during logout"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def whoami_view(request):
    if request.user.is_authenticated:
        return Response({"username": request.user.username}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def csrf_token_view(request):
    token = get_token(request)
    return Response({"csrftoken": token})


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAnonymous]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Registration successful",
                "username": serializer.data["username"],
            },
            status=status.HTTP_201_CREATED,
        )

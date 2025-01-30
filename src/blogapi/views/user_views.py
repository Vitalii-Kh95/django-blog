from django.contrib.auth import authenticate, get_user_model, login, logout
from rest_framework import generics, permissions, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from blogapi.authentication import CsrfExemptSessionAuthentication
from blogapi.permissions import IsAnonymous
from blogapi.serializers import RegistrationSerializer
from blogapi.utils import is_email


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]

    def post(self, request):
        # I removed csrf validation cause didn't like message it provided for authenticated users
        # and there seems to be no need in csrf validation for unauthenticated users.
        # As for providing csrf token in cookies, it's implicitly done via django's login function
        # as it calls to rotate_token function
        if request.user.is_authenticated:
            return Response({"detail": "You are already logged in."}, status=400)

        # @csrf_protect
        def _authenticate(request):
            User = get_user_model()
            username_or_email = request.data.get("username or email")
            password = request.data.get("password")

            # Specific error messages for missing fields
            if not username_or_email and not password:
                return Response(
                    {
                        "username or email": "This field is required.",
                        "password": "This field is required.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif not username_or_email:
                return Response(
                    {"username or email": "This field is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif not password:
                return Response(
                    {"password": "This field is required."},
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
                    {"detail": "Invalid credentials."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response(
                    {"username": user.username},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "Invalid credentials."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return _authenticate(request)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        # Log the error for debugging
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Logout error: {e}")
        return Response(
            {"detail": "Unexpected error during logout"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def whoami_view(request):
    if request.user.is_authenticated:
        return Response({"username": request.user.username}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"detail": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED
        )


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAnonymous]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "username": serializer.data["username"],
            },
            status=status.HTTP_201_CREATED,
        )

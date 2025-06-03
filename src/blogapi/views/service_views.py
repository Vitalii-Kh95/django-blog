from django.db import connections
from django.db.utils import OperationalError
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


@api_view(["GET", "HEAD"])
def api_root(request, format=None):
    """
    List of all available API endpoints.
    """
    return Response(
        data={
            "posts": {
                "list": reverse("blogapi:posts-list", request=request, format=format)
                + "?limit=6&offset=0",
                "detail": reverse(
                    "blogapi:posts-detail",
                    kwargs={"slug": "example-slug"},
                    request=request,
                    format=format,
                ),
            },
            "projects": {
                "list": reverse("blogapi:projects-list", request=request, format=format)
                + "?limit=6&offset=0",
                "detail": reverse(
                    "blogapi:projects-detail",
                    kwargs={"slug": "example-slug"},
                    request=request,
                    format=format,
                ),
            },
            "tags": reverse("blogapi:tags-list", request=request, format=format),
            "csrf_token": reverse("blogapi:csrf-token", request=request, format=format),
            "login": reverse("blogapi:login", request=request, format=format),
            "logout": reverse("blogapi:logout", request=request, format=format),
            "whoami": reverse("blogapi:whoami", request=request, format=format),
            "register": reverse("blogapi:register", request=request, format=format),
            "health": reverse("blogapi:health-check", request=request, format=format),
        },
        status=status.HTTP_200_OK,
    )


class HealthCheckView(APIView):
    """
    Check availability of service.
    """

    def get(self, request):
        db_status = "ok"
        try:
            # Check if the default database connection is active
            connections["default"].cursor()
        except OperationalError:
            db_status = "error"

        # Return the status as a JSON response
        return Response(
            {"db_status": db_status},
            status=status.HTTP_200_OK
            if db_status == "ok"
            else status.HTTP_503_SERVICE_UNAVAILABLE,
        )


@api_view(["GET", "HEAD"])
@ensure_csrf_cookie
def csrf_token_view(request):
    """
    Return the CSRF token for the current session.
    """
    token = get_token(request)
    return Response({"csrftoken": token})


@csrf_exempt
def catch_all_404_view(request, *args, **kwargs):
    """
    Custom 404 handler for unmatched or malformed URLs.
    """
    response = Response(
        {"detail": "The requested API endpoint was not found."},
        status=status.HTTP_404_NOT_FOUND,
    )
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    response.render()
    return response

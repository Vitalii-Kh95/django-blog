from django.db import connections
from django.db.utils import OperationalError
from django.middleware.csrf import get_token
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        data={
            "posts": {
                "list": reverse("blogapi:posts-list", request=request, format=format),
                "detail": reverse(
                    "blogapi:posts-detail",
                    kwargs={"slug": "example-slug"},
                    request=request,
                    format=format,
                ),
            },
            "projects": {
                "list": reverse(
                    "blogapi:projects-list", request=request, format=format
                ),
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
    API View to check the health of the database connection.
    """

    def get(self, request):
        db_status = "ok"
        try:
            # Check if the default database connection is active
            connections["default"].cursor()
        except OperationalError:
            db_status = "Unhealthy"

        # Return the status as a JSON response
        return Response(
            {"db_status": db_status},
            status=status.HTTP_200_OK
            if db_status == "Healthy"
            else status.HTTP_503_SERVICE_UNAVAILABLE,
        )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def csrf_token_view(request):
    token = get_token(request)
    return Response({"csrftoken": token})

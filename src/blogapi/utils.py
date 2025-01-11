import re

from django.forms import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def is_email(input_string):
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, input_string) is not None


# Helper function for consistent response format
def create_response(success, error=None, data=None, status_code=status.HTTP_200_OK):
    """
    Create a consistent response format.

    Args:
        success (bool): Indicates if the response represents a successful operation.
        error (str or None): Error message if success is False.
        data (dict or list or None): Data payload for successful responses.
        status_code (int): HTTP status code.

    Returns:
        Response: DRF Response object with consistent structure.
    """
    return Response(
        {"success": success, "error": error, "data": data}, status=status_code
    )


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF views.
    """
    # Call DRF's default exception handler
    response = exception_handler(exc, context)

    if response is None:
        # For exceptions not handled by DRF, provide a generic error response
        return Response(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Customize specific exceptions
    if isinstance(exc, ValidationError):
        response.data = {
            "error": "Invalid data provided.",
            "details": response.data,
        }

    return response

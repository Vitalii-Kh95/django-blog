import re

from rest_framework.views import exception_handler


def is_email(input_string):
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, input_string) is not None


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF views.
    """
    # Call DRF's default exception handler
    response = exception_handler(exc, context)

    # Check if the response contains validation errors
    if response is not None and isinstance(response.data, dict):
        for key, value in response.data.items():
            # If the value is a list, convert it to a plain string
            # I decided to do this just for the sake of consistency in the response format
            if isinstance(value, list) and len(value) == 1:
                response.data[key] = value[0]

    return response

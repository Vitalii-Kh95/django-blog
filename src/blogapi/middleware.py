from django.http import JsonResponse


class CustomAppendSlashMiddleware:
    """
    Middleware to handle missing trailing slashes for certain HTTP methods
    and return JSON responses instead of HTML errors.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check requests that don't end with a slash
        if not request.path.endswith("/"):
            # HTTP methods that require a trailing slash
            methods_needing_slash = {"POST", "PUT", "PATCH", "DELETE"}

            if request.method in methods_needing_slash:
                return JsonResponse(
                    {"detail": "Trailing slash missing from URL."}, status=400
                )

        # Proceed with the normal request processing
        return self.get_response(request)

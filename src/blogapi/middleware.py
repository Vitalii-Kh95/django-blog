from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class CustomAppendSlashMiddleware:
    """
    Middleware to handle missing trailing slashes for certain HTTP methods
    and return JSON responses instead of HTML errors.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude media URLs and any other URLs that should not have a trailing slash check
        if request.path.startswith("/media/"):
            return self.get_response(request)

        # Only check requests that don't end with a slash
        if not request.path.endswith("/"):
            # HTTP methods that require a trailing slash

            response = Response(
                {"detail": "Trailing slash missing from URL."}, status=400
            )
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            response.render()
            return response

        # Proceed with the normal request processing
        return self.get_response(request)

from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


def global_404_handler(request, exception=None):
    """
    Global 404 handler for the entire project.
    Handles API and non-API paths separately.
    Prioritizes JSON for API paths if both JSON and HTML are acceptable.
    """
    api_prefix = f"/{settings.API_PATH_PREFIX}/"

    def render_json_response(data, status_code):
        """Helper to create and render a JSON response."""
        response = Response(data, status=status_code)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        return response

    if request.path.startswith(api_prefix):
        # Check the Accept header
        accept_header = request.headers.get("Accept", "")

        if "application/json" in accept_header:
            # Prioritize JSON for API consumers
            return render_json_response(
                {"detail": "The requested API endpoint was not found."},
                status.HTTP_404_NOT_FOUND,
            )

        if "text/html" in accept_header:
            # Render the HTML 404 page for browsers
            return render(request, "404.html", status=404)

        # Default to JSON for ambiguous or missing Accept headers
        return render_json_response(
            {"detail": "The requested API endpoint was not found."},
            status.HTTP_404_NOT_FOUND,
        )

    # Render a custom HTML 404 page for non-API requests
    print(request.headers)
    return render(request, "404.html", status=404)

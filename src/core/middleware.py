import json
import logging

logger = logging.getLogger("request_response")


class LogRequestResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request
        request_info = {
            "method": request.method,
            "path": request.get_full_path(),
            "headers": dict(request.headers),
        }

        if request.content_type == "application/json" and request.body:
            try:
                request_info["body"] = json.loads(request.body)
            except json.JSONDecodeError:
                request_info["body"] = "Request body is not JSON serializable"
        elif request.content_type.startswith("multipart/form-data"):
            try:
                parts = {}
                for key, value in request.POST.items():
                    parts[key] = value
                for key, value in request.FILES.items():
                    parts[key] = {
                        "filename": value.name,
                        "content_type": value.content_type,
                        "size": value.size,
                    }
                request_info["body"] = parts
            except Exception as e:
                request_info["body"] = f"Failed to parse multipart form data: {e}"
        else:
            request_info["body"] = request.body.decode("utf-8", errors="replace")

        logger.info("Request: %s", json.dumps(request_info, indent=4))

        response = self.get_response(request)

        # Log the response
        response_info = {
            "status_code": response.status_code,
            "headers": dict(response.items()),
        }

        if response["Content-Type"] == "application/json":
            try:
                response_info["body"] = json.loads(response.content)
            except json.JSONDecodeError:
                response_info["body"] = "Response body is not JSON serializable"
        else:
            response_info["body"] = response.content.decode("utf-8", errors="replace")

        logger.info("Response: %s", json.dumps(response_info, indent=4))

        return response

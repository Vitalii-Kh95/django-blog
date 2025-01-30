from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """Needed to exempt csrf validation for some views"""

    def enforce_csrf(self, request):
        pass  # Don't enforce CSRF validation

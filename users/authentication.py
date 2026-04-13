"""Custom JWT authentication using HTTP-only cookies for token transport."""

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class CookieJWTAuthentication(JWTAuthentication):
    """Reads the access token from an HTTP-only cookie instead of a header."""

    def authenticate(self, request):
        """Reads access_token cookie and authenticates the request."""
        raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            return None
        try:
            validated_token = self.get_validated_token(raw_token)
        except (InvalidToken, TokenError):
            return None
        return self.get_user(validated_token), validated_token

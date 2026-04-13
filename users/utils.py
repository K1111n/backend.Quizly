"""Helper functions for the users app."""

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import UserSerializer


def set_auth_cookies(response, access_token, refresh_token):
    """Sets the JWT access and refresh tokens as HTTP-only cookies."""
    response.set_cookie(
        'access_token', access_token, httponly=True, samesite='Lax'
    )
    response.set_cookie(
        'refresh_token', refresh_token, httponly=True, samesite='Lax'
    )


def delete_auth_cookies(response):
    """Removes the JWT access and refresh token cookies from the response."""
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')


def apply_refresh_cookies(response, token_data):
    """Applies refreshed token(s) as HTTP-only cookies to the response."""
    response.set_cookie(
        'access_token', token_data['access'], httponly=True, samesite='Lax'
    )
    if 'refresh' in token_data:
        response.set_cookie(
            'refresh_token', token_data['refresh'],
            httponly=True, samesite='Lax',
        )


def blacklist_refresh_token(token_string):
    """Blacklists the given refresh token; silently ignores invalid tokens."""
    if not token_string:
        return
    try:
        token = RefreshToken(token_string)
        token.blacklist()
    except TokenError:
        pass


def build_login_response_body(user):
    """Returns the login success response body as a dict."""
    return {
        'detail': 'Login successfully!',
        'user': UserSerializer(user).data,
    }

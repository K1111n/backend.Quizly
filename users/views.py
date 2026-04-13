"""Views for the users app — authentication endpoints."""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate

from .serializers import RegisterSerializer
from .utils import (
    set_auth_cookies,
    delete_auth_cookies,
    apply_refresh_cookies,
    blacklist_refresh_token,
    build_login_response_body,
)

LOGOUT_SUCCESS_MSG = (
    'Log-Out successfully! All Tokens will be deleted. '
    'Refresh token is now invalid.'
)


class RegisterView(APIView):
    """Registers a new user account."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Creates a new user if the provided data is valid."""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': 'User created successfully!'},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """Authenticates a user and issues JWT tokens via HTTP-only cookies."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Validates credentials, sets auth cookies, and returns user data."""
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid credentials.')
        refresh = RefreshToken.for_user(user)
        response = Response(build_login_response_body(user))
        set_auth_cookies(response, str(refresh.access_token), str(refresh))
        return response


class LogoutView(APIView):
    """Logs out the authenticated user and invalidates all tokens."""

    def post(self, request):
        """Blacklists the refresh token and clears auth cookies."""
        blacklist_refresh_token(request.COOKIES.get('refresh_token'))
        response = Response({'detail': LOGOUT_SUCCESS_MSG})
        delete_auth_cookies(response)
        return response


class TokenRefreshView(APIView):
    """Issues a new access token using a valid refresh token cookie."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Reads refresh_token cookie and returns a new access token."""
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            raise AuthenticationFailed('No refresh token provided.')
        serializer = TokenRefreshSerializer(data={'refresh': refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise AuthenticationFailed(str(e))
        response = Response({'detail': 'Token refreshed'})
        apply_refresh_cookies(response, serializer.validated_data)
        return response

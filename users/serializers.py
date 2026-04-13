"""Serializers for the users app."""

from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration with password confirmation."""

    password = serializers.CharField(write_only=True)
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']

    def validate_email(self, value):
        """Validates that the email address is not already in use."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already in use.')
        return value

    def validate(self, data):
        """Validates that both password fields match."""
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError(
                {'confirmed_password': 'Passwords do not match.'}
            )
        return data

    def create(self, validated_data):
        """Creates and returns a new user without the confirmation field."""
        validated_data.pop('confirmed_password')
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Read-only serializer for returning user information."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

"""Serializers for the quizzes app."""

from rest_framework import serializers
from .models import Quiz, Question


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for individual quiz questions."""

    class Meta:
        model = Question
        fields = [
            'id', 'question_title', 'question_options',
            'answer', 'created_at', 'updated_at',
        ]


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for quizzes, including nested questions.

    Only `title` and `description` are writable; all other fields are
    read-only.
    """

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description',
            'created_at', 'updated_at',
            'video_url', 'questions',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'video_url']

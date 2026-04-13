"""Views for the quizzes app — quiz CRUD and generation endpoints."""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError

from .models import Quiz
from .serializers import QuizSerializer
from .utils import process_youtube_url, get_user_quiz


class QuizListCreateView(APIView):
    """Lists the user's quizzes or creates a new one from a YouTube URL."""

    def get(self, request):
        """Returns all quizzes belonging to the authenticated user."""
        queryset = Quiz.objects.filter(user=request.user)
        serializer = QuizSerializer(
            queryset.order_by('-created_at'), many=True
        )
        return Response(serializer.data)

    def post(self, request):
        """Creates a new quiz from the provided YouTube URL."""
        url = request.data.get('url')
        if not url:
            raise ValidationError({'url': 'This field is required.'})
        try:
            quiz = process_youtube_url(request.user, url)
        except Exception as e:
            raise APIException(detail=str(e))
        return Response(
            QuizSerializer(quiz).data,
            status=status.HTTP_201_CREATED,
        )


class QuizDetailView(APIView):
    """Retrieves, partially updates, or deletes a specific quiz."""

    def get(self, request, pk):
        """Returns the quiz with the given ID if it belongs to the user."""
        quiz = get_user_quiz(request.user, pk)
        return Response(QuizSerializer(quiz).data)

    def patch(self, request, pk):
        """Partially updates the quiz title and/or description."""
        quiz = get_user_quiz(request.user, pk)
        serializer = QuizSerializer(quiz, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        """Permanently deletes the quiz and all its questions."""
        quiz = get_user_quiz(request.user, pk)
        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

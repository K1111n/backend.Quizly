"""Admin configuration for the quizzes app."""

from django.contrib import admin
from .models import Quiz, Question


class QuestionInline(admin.TabularInline):
    """Inline editor for questions within the quiz admin view."""

    model = Question
    extra = 0
    fields = ['question_title', 'question_options', 'answer']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin view for quizzes with inline question editing."""

    list_display = ['title', 'user', 'created_at', 'updated_at']
    list_filter = ['user', 'created_at']
    search_fields = ['title', 'description']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin view for individual questions."""

    list_display = ['question_title', 'quiz', 'answer']
    list_filter = ['quiz']
    search_fields = ['question_title', 'answer']

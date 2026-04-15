"""Helper functions: audio download, Whisper transcription, quiz generation."""

import os
import re
import json
import tempfile
import shutil

import yt_dlp
import whisper
from django.conf import settings
from google import genai
from rest_framework.exceptions import NotFound, PermissionDenied

from .models import Quiz, Question


_YOUTUBE_PATTERN = re.compile(
    r'^(https?://)?(www\.)?(youtube\.com/(watch\?v=|shorts/)|youtu\.be/)\S+'
)


def is_youtube_url(url):
    """Returns True if the given URL points to a YouTube video."""
    return bool(_YOUTUBE_PATTERN.match(url))


QUIZ_PROMPT_TEMPLATE = (
    "Based on the following video transcript, "
    "create a quiz with exactly 10 questions.\n"
    "Each question must have exactly 4 answer options "
    "with exactly one correct answer.\n"
    "Respond ONLY with a valid JSON object using this exact structure:\n"
    '{{"title": "<quiz title>", "description": "<short description>", '
    '"questions": ['
    '{{"question_title": "<question>", '
    '"question_options": ["<A>", "<B>", "<C>", "<D>"], '
    '"answer": "<correct option text (must match one option exactly)>"'
    '}}]}}\n'
    "Transcript:\n{transcript}"
)


def _build_ydl_opts(output_dir):
    """Builds yt-dlp options dict for extracting audio as MP3."""
    return {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }


def download_audio(url):
    """Downloads YouTube audio via yt-dlp, returns (output_dir, mp3_path)."""
    output_dir = tempfile.mkdtemp()
    ydl_opts = _build_ydl_opts(output_dir)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        audio_path = os.path.join(output_dir, f"{info['id']}.mp3")
    return output_dir, audio_path


def transcribe_audio(audio_path):
    """Transcribes an audio file using Whisper AI and returns the text."""
    model = whisper.load_model('base')
    result = model.transcribe(audio_path)
    return result['text']


def _build_quiz_prompt(transcript):
    """Builds the Gemini prompt string from a transcript."""
    return QUIZ_PROMPT_TEMPLATE.format(transcript=transcript)


def generate_quiz_data(transcript):
    """Sends the transcript to Gemini Flash, returns the parsed quiz data."""
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=_build_quiz_prompt(transcript),
        config={'response_mime_type': 'application/json'},
    )
    return json.loads(response.text)


def _build_question_objects(quiz, questions_data):
    """Returns unsaved Question instances from raw data for bulk insert."""
    return [
        Question(
            quiz=quiz,
            question_title=q['question_title'],
            question_options=q['question_options'],
            answer=q['answer'],
        )
        for q in questions_data
    ]


def save_quiz(user, url, quiz_data):
    """Saves the quiz and its questions to the database, returns the Quiz."""
    quiz = Quiz.objects.create(
        user=user,
        title=quiz_data['title'],
        description=quiz_data['description'],
        video_url=url,
    )
    questions = _build_question_objects(quiz, quiz_data['questions'])
    Question.objects.bulk_create(questions)
    return quiz


def process_youtube_url(user, url):
    """Full pipeline: download → transcribe → generate → save quiz."""
    output_dir, audio_path = download_audio(url)
    try:
        transcript = transcribe_audio(audio_path)
        quiz_data = generate_quiz_data(transcript)
        return save_quiz(user, url, quiz_data)
    finally:
        shutil.rmtree(output_dir, ignore_errors=True)


def get_user_quiz(user, pk):
    """Returns the user's quiz by pk; raises NotFound or PermissionDenied."""
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        raise NotFound('Quiz not found.')
    if quiz.user != user:
        raise PermissionDenied()
    return quiz

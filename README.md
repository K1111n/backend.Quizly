# Quizly – Backend

Django REST API for the Quizly application. Generates quizzes from YouTube videos using Whisper AI for transcription and Gemini Flash for quiz creation.

---

## Requirements

### System Dependencies

**FFmpeg** must be installed globally on your system — it is required by Whisper AI to process audio files.

- **macOS:** `brew install ffmpeg`
- **Ubuntu/Debian:** `sudo apt install ffmpeg`
- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

Verify installation: `ffmpeg -version`

### Python

Python 3.10+ is required.

---

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export SECRET_KEY="your-secret-key"
export GEMINI_API_KEY="your-gemini-api-key"

# 4. Run migrations
python manage.py migrate

# 5. Create a superuser (for the admin panel)
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver
```

---

## Environment Variables

| Variable        | Description                                      |
|-----------------|--------------------------------------------------|
| `SECRET_KEY`    | Django secret key (required in production)       |
| `GEMINI_API_KEY`| Google Gemini API key for quiz generation        |

A free Gemini API key can be obtained at [aistudio.google.com](https://aistudio.google.com).

---

## API Endpoints

| Method | Endpoint              | Description                          | Auth required |
|--------|-----------------------|--------------------------------------|---------------|
| POST   | `/api/register/`      | Register a new user                  | No            |
| POST   | `/api/login/`         | Login and receive JWT cookies        | No            |
| POST   | `/api/logout/`        | Logout and invalidate tokens         | Yes           |
| POST   | `/api/token/refresh/` | Refresh the access token             | No            |
| GET    | `/api/quizzes/`       | List all quizzes of the current user | Yes           |
| POST   | `/api/quizzes/`       | Create a new quiz from a YouTube URL | Yes           |
| GET    | `/api/quizzes/{id}/`  | Retrieve a specific quiz             | Yes           |
| PATCH  | `/api/quizzes/{id}/`  | Update quiz title or description     | Yes           |
| DELETE | `/api/quizzes/{id}/`  | Delete a quiz                        | Yes           |

Full API documentation: see `api-endpoints.md`.

---

## Authentication

Authentication is handled via **JWT tokens stored in HTTP-only cookies** (`access_token`, `refresh_token`). Tokens are automatically sent with each request by the browser.

- Access token lifetime: 15 minutes
- Refresh token lifetime: 7 days (rotated on refresh, blacklisted on logout)

---

## Admin Panel

Available at `/admin/`. Supports:
- Viewing, editing, and deleting quizzes
- Editing individual questions inline within a quiz

---

## Tech Stack

- **Django 6** + **Django REST Framework**
- **SimpleJWT** – JWT authentication
- **yt-dlp** – YouTube audio download
- **Whisper AI** – local audio transcription (OpenAI)
- **Gemini Flash** – AI quiz generation (Google)
- **FFmpeg** – audio processing (system dependency)

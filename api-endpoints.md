# Quizly API Endpoints

## Authentication

### POST `/api/register/`
Registriert einen neuen Benutzer.

**Request Body**
```json
{
  "username": "your_username",
  "password": "your_password",
  "confirmed_password": "your_confirmed_password",
  "email": "your_email@example.com"
}
```

**Response `201`**
```json
{
  "detail": "User created successfully!"
}
```

**Status Codes**
| Code | Beschreibung |
|------|--------------|
| 201  | Benutzer erfolgreich erstellt |
| 400  | Ungültige Daten |
| 500  | Interner Serverfehler |

**Permissions:** Keine

---

### POST `/api/login/`
Meldet den Benutzer an und setzt Auth-Cookies.

**Request Body**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response `200`**
```json
{
  "detail": "Login successfully!",
  "user": {
    "id": 1,
    "username": "your_username",
    "email": "your_email@example.com"
  }
}
```

**Status Codes**
| Code | Beschreibung |
|------|--------------|
| 200  | Erfolgreicher Login |
| 401  | Ungültige Anmeldedaten |
| 500  | Interner Serverfehler |

**Permissions:** Keine
**Hinweis:** Setzt `access_token` und `refresh_token` als Cookies.

---

### POST `/api/logout/`
Meldet den Benutzer ab und löscht alle Token.

**Request Body:** Leer

**Response `200`**
```json
{
  "detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."
}
```

**Status Codes**
| Code | Beschreibung |
|------|--------------|
| 200  | Erfolgreicher Logout |
| 401  | Nicht authentifiziert |
| 500  | Interner Serverfehler |

**Permissions:** Authentifizierung erforderlich
**Hinweis:** Cookies `access_token` und `refresh_token` werden entfernt.

---

### POST `/api/token/refresh/`
Erneuert den Access-Token mithilfe des Refresh-Tokens.

**Request Body:** Leer

**Response `200`**
```json
{
  "detail": "Token refreshed"
}
```

**Status Codes**
| Code | Beschreibung |
|------|--------------|
| 200  | Token erfolgreich erneuert |
| 401  | Refresh Token ungültig oder fehlt |
| 500  | Interner Serverfehler |

**Permissions:** Authentifizierung über `refresh_token`-Cookie erforderlich
**Hinweis:** Setzt neuen `access_token` Cookie.

---

## Quiz Management

### POST `/api/quizzes/`
Erstellt ein neues Quiz basierend auf einer YouTube-URL.

**Request Body**
```json
{
  "url": "https://www.youtube.com/watch?v=example"
}
```

**Response `201`**
```json
{
  "id": 1,
  "title": "Quiz Title",
  "description": "Quiz Description",
  "created_at": "2023-07-29T12:34:56.789Z",
  "updated_at": "2023-07-29T12:34:56.789Z",
  "video_url": "https://www.youtube.com/watch?v=example",
  "questions": [
    {
      "id": 1,
      "question_title": "Question 1",
      "question_options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Option A",
      "created_at": "2023-07-29T12:34:56.789Z",
      "updated_at": "2023-07-29T12:34:56.789Z"
    }
  ]
}
```

**Status Codes**
| Code | Beschreibung |
|------|--------------|
| 201  | Quiz erfolgreich erstellt |
| 400  | Ungültige URL oder Anfragedaten |
| 401  | Nicht authentifiziert |
| 500  | Interner Serverfehler |

**Permissions:** Authentifizierung erforderlich

---

### GET `/api/quizzes/`
Ruft alle Quizzes des authentifizierten Benutzers ab.

**Response `200`**
```json
[
  {
    "id": 1,
    "title": "Quiz Title",
    "description": "Quiz Description",
    "created_at": "2023-07-29T12:34:56.789Z",
    "updated_at": "2023-07-29T12:34:56.789Z",
    "video_url": "https://www.youtube.com/watch?v=example",
    "questions": [
      {
        "id": 1,
        "question_title": "Question 1",
        "question_options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "Option A"
      }
    ]
  }
]
```

**Status Codes**
| Code | Beschreibung |
|------|--------------|
| 200  | Quizzes erfolgreich abgerufen |
| 401  | Nicht authentifiziert |
| 500  | Interner Serverfehler |

**Permissions:** Authentifizierung erforderlich

---

### GET `/api/quizzes/{id}/`
Ruft ein spezifisches Quiz des Benutzers ab.

**URL Parameter:** `id` — Die ID des Quiz.

**Response `200`**
```json
{
  "id": 1,
  "title": "Quiz Title",
  "description": "Quiz Description",
  "created_at": "2023-07-29T12:34:56.789Z",
  "updated_at": "2023-07-29T12:34:56.789Z",
  "video_url": "https://www.youtube.com/watch?v=example",
  "questions": [
    {
      "id": 1,
      "question_title": "Question 1",
      "question_options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Option A"
    }
  ]
}
```

**Status Codes**
| Code | Beschreibung |
|------|--------------|
| 200  | Quiz erfolgreich abgerufen |
| 401  | Nicht authentifiziert |
| 403  | Zugriff verweigert – Quiz gehört nicht dem Benutzer |
| 404  | Quiz nicht gefunden |
| 500  | Interner Serverfehler |

**Permissions:** Authentifizierung erforderlich. Benutzer kann nur eigene Quizzes abrufen.

---

### PATCH `/api/quizzes/{id}/`
Aktualisiert einzelne Felder eines Quiz (partielle Aktualisierung).

**URL Parameter:** `id` — Die ID des Quiz.

**Request Body**
```json
{
  "title": "Partially Updated Title",
  "description": "Partially Updated Description"
}
```

**Response `200`**
```json
{
  "id": 1,
  "title": "Partially Updated Title",
  "description": "Quiz Description",
  "created_at": "2023-07-29T12:34:56.789Z",
  "updated_at": "2023-07-29T14:45:12.345Z",
  "video_url": "https://www.youtube.com/watch?v=example",
  "questions": [
    {
      "id": 1,
      "question_title": "Question 1",
      "question_options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Option A"
    }
  ]
}
```

**Status Codes**
| Code | Beschreibung |
|------|--------------|
| 200  | Quiz erfolgreich aktualisiert |
| 400  | Ungültige Anfragedaten |
| 401  | Nicht authentifiziert |
| 403  | Zugriff verweigert – Quiz gehört nicht dem Benutzer |
| 404  | Quiz nicht gefunden |
| 500  | Interner Serverfehler |

**Permissions:** Authentifizierung erforderlich. Benutzer kann nur eigene Quizzes bearbeiten.

---

### DELETE `/api/quizzes/{id}/`
Löscht ein Quiz und alle zugehörigen Fragen permanent.

**URL Parameter:** `id` — Die ID des Quiz.

**Response:** `204 No Content`

**Status Codes**
| Code | Beschreibung |
|------|--------------|
| 204  | Quiz erfolgreich gelöscht |
| 401  | Nicht authentifiziert |
| 403  | Zugriff verweigert – Quiz gehört nicht dem Benutzer |
| 404  | Quiz nicht gefunden |
| 500  | Interner Serverfehler |

**Permissions:** Authentifizierung erforderlich. Benutzer kann nur eigene Quizzes löschen.
**Warnung:** Das Löschen ist permanent und kann nicht rückgängig gemacht werden.

# HeartServer
**HeartServer** is a **Django REST Framework (DRF)** backend API for a multiplayer card game called **Heart Game**. It provides secure user authentication, game session management, real-time gameplay logic, and scalable RESTful endpoints — all built with best practices in DRF.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-4.2%2B-green)
![DRF](https://img.shields.io/badge/DRF-3.14%2B-red)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Features
- **User Authentication** with JWT (Registration, Login, Token Refresh)
- **Game Session Management** (Create, Join, Play, Track Turns)
- **Full CRUD Operations** via DRF `ViewSets` and `Routers`
- **Custom Serializers** with validation and nested relationships
- **Permission Classes** (Owner-only, Game Participant, Authenticated)
- **Browsable API** with DRF's built-in UI
- **Modular App Structure** (`user/`, `game/`)

---

## Tech Stack

| Technology                  | Version     |
|-----------------------------|-------------|
| Python                      | 3.10+       |
| Django                      | 4.2+        |
| Django REST Framework       | 3.14+       |
| SimpleJWT                   | Latest      |
| SQLite (dev) / PostgreSQL (prod) | —       |

---

## Project Structure
```
HeartServer/
├── HeartServer/            # Project settings & URLs
│   ├── settings.py
│   ├── urls.py             # Includes DRF router
│   └── wsgi.py
├── game/                   # Game logic app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py (optional)
│   └── permissions.py
├── user/                   # User management app
│   ├── models.py
│   ├── serializers.py
│   └── views.py
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md               # You are here!
```

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/charitraa/HeartServer.git
cd HeartServer
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the root:
```env
SECRET_KEY=your-super-secret-django-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=7
```

### 5. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Server
```bash
python manage.py runserver
```
API will be available at: `http://127.0.0.1:8000/`

---

## API Endpoints (DRF)

### Authentication (`/api/auth/`)
| Method | Endpoint | Description |
|---------|-----------|-------------|
| POST | `/user/create/` | Register user |
| POST | `/user/login/` | Get JWT tokens |
| GET | `/user/me/` | User profile |

> **Note:** Authentication required for game actions.

---

## DRF Configuration (Best Practices)

### `settings.py`
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
```
---

## Testing
Use DRF's **Browsable API** or tools like **Postman / Insomnia**.  
Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Contributing
1. Fork the repo  
2. Create your branch: `git checkout -b feature/xyz`  
3. Commit: `git commit -m "Add xyz"`  
4. Push: `git push origin feature/xyz`  
5. Open a Pull Request  

---

## Recent Updates
- ✅ Yesterday – Updated views and serializers  
- ✅ 2 days ago – Completed game module  
- ✅ Last week – Server setup and .gitignore  
- ✅ 2 days ago – Updated requirements.txt  

---

## License
This project is licensed under the **MIT License**. See `LICENSE` for details.

---

## Contact
**Maintainer:** [charitraa](https://github.com/charitraa)  
**Game:** Heart Game (Cards)  

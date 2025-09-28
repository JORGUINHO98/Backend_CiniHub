import os
import dj_database_url
from pathlib import Path
from django.core.management.utils import get_random_secret_key
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# Configuración básica
# ========================
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key())
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

# Incluye IP pública, localhost y 127.0.0.1
ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "3.12.189.221,localhost,127.0.0.1"
).split(",")

# ========================
# Aplicaciones
# ========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "cineapp",
]

AUTH_USER_MODEL = "cineapp.Usuario"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cinehub_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cinehub_project.wsgi.application"

# ========================
# Base de datos
# ========================
DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get(
            "DATABASE_URL", "postgres://cinehub_user:superpassword@db:5432/cinehub"
        ),
        conn_max_age=600,
    )
}

# ========================
# Cache (Redis)
# ========================
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://redis:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "cinehub",
        "TIMEOUT": 300,
    }
}

# ========================
# Archivos estáticos
# ========================
STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ========================
# DRF + JWT
# ========================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# ========================
# TMDB
# ========================
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")

# ========================
# CORS
# ========================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:19006",
    "http://127.0.0.1:19006",
    "http://192.168.0.10:19006",  # Expo web
    "http://localhost:8081",
    "http://127.0.0.1:8081",
    "http://192.168.0.10:8081",
    "http://localhost:8082",
    "http://127.0.0.1:8082",
    "http://192.168.0.10:8082",  # Expo dev web
    "http://3.12.189.221",        # AWS backend para producción
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8050",
    "http://127.0.0.1:8050",
    "http://192.168.0.10:8050",
    "http://3.12.189.221",        # AWS para requests con CSRF
]

# ========================
# Seguridad básica
# ========================
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
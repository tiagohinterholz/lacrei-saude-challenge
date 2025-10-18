import os
import sys
from dotenv import load_dotenv
from corsheaders.defaults import default_headers
from datetime import timedelta

# ===================== BASE =====================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# ===================== CONFIG BÁSICA =====================
SECRET_KEY = os.getenv("SECRET_KEY", "dummy-secret-key-for-ci-only")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "lacrei-saude-prod.eba-bc8hq6yk.us-east-2.elasticbeanstalk.com,3.150.184.244").split(",")

# ===================== CORS =====================
CORS_ALLOW_HEADERS = list(default_headers) + ["X-Register"]

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")

CORS_ALLOW_CREDENTIALS = True

# ===================== LOGS =====================
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} [{levelname}] {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "app.log"),
            "when": "midnight",
            "backupCount": 7,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {"handlers": ["console", "file"], "level": "INFO"},
        "django.request": {"handlers": ["console", "file"], "level": "ERROR", "propagate": False},
        "apps": {"handlers": ["file"], "level": "INFO", "propagate": True},
    },
}

# ===================== APLICATIVOS =====================
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django_extensions"
]

THIRD_APPS = ["corsheaders", "gunicorn"]

PROJECT_APPS = [
    "apps.common",
    "apps.professionals",
    "apps.appointments",
    "apps.users",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + PROJECT_APPS

# ===================== MIDDLEWARE =====================
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

# ===================== SEGURANÇA EXTRA =====================
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"

# ===================== TEMPLATES E WSGI =====================
ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "apps", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# ===================== BANCO DE DADOS =====================
DATABASES = {
    "default": {
        "ENGINE": os.getenv("ENGINE_DB", "django.db.backends.sqlite3"),
        "NAME": os.getenv("NAME_DB", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.getenv("USER_DB", ""),
        "PASSWORD": os.getenv("PASSWORD_DB", ""),
        "HOST": os.getenv("HOST_DB", ""),
        "PORT": os.getenv("PORT_DB", ""),
    }
}

# ===================== USUÁRIOS =====================
AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ===================== REST FRAMEWORK / JWT =====================
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "COERCE_DECIMAL_TO_STRING": False,
}

APPEND_SLASH = True

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ===================== DOCUMENTAÇÃO =====================
SPECTACULAR_SETTINGS = {
    "TITLE": "Lacrei Saúde API",
    "DESCRIPTION": "API desenvolvida para o desafio técnico da Lacrei Saúde.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_AUTHENTICATION": [],
    "COMPONENT_SPLIT_REQUEST": True,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "SECURITY": [{"BearerAuth": []}],
    "COMPONENTS": {
        "securitySchemes": {
            "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        }
    },
}

# ===================== INTERNACIONALIZAÇÃO =====================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ===================== ARQUIVOS ESTÁTICOS / MÍDIA =====================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===================== LOGIN / LOGOUT =====================
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# ===================== REQUEST LOGS =====================
REQUESTLOGS = {
    "SECRETS": ["password", "token"],
    "METHODS": ["PUT", "PATCH", "POST", "DELETE"],
}
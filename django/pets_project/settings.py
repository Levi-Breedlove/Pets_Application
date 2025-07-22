# settings.py (trimmed)

from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------ Core
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-insecure-key")
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"

if DEBUG:
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS = [
        'https://*.amazonaws.com', 
        'http://127.0.0.1', 
        'http://localhost', 
        'http://*.elasticbeanstalk.com',  
        'https://localhost:8000',
        'https://127.0.0.1:8000'
    ]
else:
    ALLOWED_HOSTS = [
        os.getenv("PRIMARY_HOST", "pets-app.example.com"),
        ".elasticbeanstalk.com",  # wildcard
    ]
    CSRF_TRUSTED_ORIGINS = [
        f"https://{os.getenv('PRIMARY_HOST', 'pets-app.example.com')}",
        "https://*.elasticbeanstalk.com",
    ]

# ------------------------------------------------------------------ Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pets_app",
]

# ------------------------------------------------------------------ Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
   # "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pets_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # add if you plan project-level templates
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

WSGI_APPLICATION = "pets_project.wsgi.application"

# ------------------------------------------------------------------ DB
if os.getenv("USE_SQLITE", "1") == "1":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME", "pets"),
            "USER": os.getenv("DB_USER", "django"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "3306"),
            "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
        }
    }

# ------------------------------------------------------------------ i18n / TZ
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Los_Angeles"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------ Static & media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static_root"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------------------------------------------ Storage switch
USE_S3 = os.getenv("USE_S3", "0") == "1"
if USE_S3:
    INSTALLED_APPS += ["storages"]
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = os.getenv("AWS_REGION", "us-west-2")
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    STORAGES = {
        "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
        "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"},
    }
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

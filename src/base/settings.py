"""
Django settings for Yamtrack project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from decouple import config, Csv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET", default="secret")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

INTERNAL_IPS = ["127.0.0.1"]

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=Csv())

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

if config("HTTPS_COOKIES", default=False, cast=bool):
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Application definition

INSTALLED_APPS = [
    "app",
    "crispy_forms",
    "crispy_bootstrap5",
    "sass_processor",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
]

ADMIN_ENABLED = config("ADMIN_ENABLED", default=False, cast=bool)

if ADMIN_ENABLED:
    INSTALLED_APPS.append("django.contrib.admin")

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "base.urls"

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
                "django.template.context_processors.media",
                "app.context_processors.export_vars",
            ],
        },
    },
]

WSGI_APPLICATION = "base.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if config("DB_HOST", default=None):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": config("DB_HOST"),
            "NAME": config("DB_NAME", default="yamtrack"),
            "USER": config("DB_USER", default="yamtrack"),
            "PASSWORD": config("DB_PASSWORD", default="yamtrack"),
            "PORT": config("DB_PORT", default="5432"),
        }
    }
else:
    # create db folder if it doesn't exist
    os.makedirs(os.path.join(BASE_DIR, "db"), exist_ok=True)

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db/db.sqlite3"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Logging
# https://docs.djangoproject.com/en/4.0/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        'asyncio': {
            'level': 'WARNING',
        },
    },
    "formatters": {
        "verbose": {
            "format": "{asctime:<21} {levelname:<7} [{filename}:{lineno}] {message}",
            # 2023-03-15T21:27:37Z format
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "level": "DEBUG" if DEBUG else "INFO",
        },
    },
    "root": {"handlers": ["console"], "level": "DEBUG" if DEBUG else "INFO"},
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = config("TZ", default="UTC")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
MEDIA_URL = "media/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "home"

LOGOUT_REDIRECT_URL = "login"

AUTH_USER_MODEL = "app.User"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, "app/static")

SASS_OUTPUT_STYLE = "compact"

DEBUG_TOOLBAR_CONFIG = {
    "SKIP_TEMPLATE_PREFIXES": ("app/include/"),
}

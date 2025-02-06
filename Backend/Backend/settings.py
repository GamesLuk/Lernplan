"""
Django settings for Backend project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o)0dt!(f2+)#crrn&s_(bnhgz27qlun=4)!&ar$^@f^fzraq%w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',             # Preset
    'django.contrib.auth',              # Preset
    'django.contrib.contenttypes',      # Preset
    'django.contrib.sessions',          # Preset
    'django.contrib.messages',          # Preset
    'django.contrib.staticfiles',       # Preset
    "main",                             # App
    "auth_user",                        # App
    "system",                           # App
    "django_celery_beat",            # Celery
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "middleware.system_middleware.MultipleProxyMiddleware",     # Host-Erkennung
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"templates"], # Pfad für eigene Templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lernplan',  # Name der Datenbank
        'USER': 'System',     # MySQL-Benutzername
        'PASSWORD': '5f7%@#gj8J&Sqeu3YjGq',  # MySQL-Passwort
        'HOST': 'localhost',  # MySQL-Host (standardmäßig localhost)
        'PORT': '3306',       # MySQL-Port (standardmäßig 3306)
        'CONN_MAX_AGE': 600,  # Verbindungen bleiben 5 Minuten offen
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    '127.0.0.1',  # Lokale IP-Adresse
]

ALLOWED_HOSTS = [
    "mzb-lev.de",
    ".mzb-lev.de",      # Alle Subdomains
    "localhost",
    "127.0.0.1",
]

USE_X_FORWARDED_HOST = True                                     # Für Host-Erkennung

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')   # Für Host-Erkennung

MICROSOFT_CLIENT_ID = 'c6cb3ad8-1a5e-4a74-98b5-a35ddd029c31'
MICROSOFT_CLIENT_SECRET = 'QUm8Q~z2OvxQ20IgrKkkgcsYh7hI3ZxBFoIZwavz'
MICROSOFT_REDIRECT_URI = 'https://mzb-lev.de/accounts/microsoft/callback/'
MICROSOFT_AUTHORIZATION_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
MICROSOFT_TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
MICROSOFT_USER_INFO_URL = 'https://graph.microsoft.com/v1.0/me'

SCOPES = [                      # Für Microsoft-Login (Berechtigungen)
    "openid",                   # Save
    "email",                    # Save
    "profile",                  # Save
    "offline_access",           # Save
    "User.Read",
    "Team.ReadBasic.All",
    "User.ReadBasic.All",
    "Directory.Read.All",       # evt Falsch
    "GroupMember.Read.All",     # evt Falsch
    "TeamMember.Read.All",      # evt Falsch
    "User.Read.All",            # evt Falsch

]

# Redis als Broker für Celery
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/1"

# Cache mit Redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# ----------------------------------------------------------------------------------------------------

REQUESTED_URL_NAME = "requested_url_dfg"

SCHUL_IDS = "8bf5190c-b458-41c9-9cc2-631ff5956148"

CHECK_SCHUL_IDS = True     # Default: TRUE | Test: FALSE

TOKEN = "fkji4hht4iifgndfkg"
from os import getenv as env
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('SECRET_KEY', 'django-insecure-Django_secret_key_Django_secret_key_Django_secret')

DEBUG = env('DEBUG') == 'True'

ALLOWED_HOSTS = env('ALLOWED_HOSTS', '127.0.0.1:8000,localhost').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'djoser',
    'colorfield',
    'api.apps.ApiConfig',
    'users.apps.UsersConfig',
    'food.apps.FoodConfig',
]

# Users settings
AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000'
]

# Use sql in debug mode and postgers in production(on server)

DATABASE = env("DATABASE", 'POSTGRES')
DATABASES = {
    'default': {
        'SQLITE': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
        'POSTGRES': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('POSTGRES_DB', 'django'),
            'USER': env('POSTGRES_USER', 'django'),
            'PASSWORD': env('POSTGRES_PASSWORD', ''),
            'HOST': env('POSTGRES_HOST', ''),
            'PORT': env('POSTGRES_PORT', 5432)
        }
    }[DATABASE]
}


DATA_UPLOAD_MAX_NUMBER_FIELDS = 3000

# models settings
USER_EMAIL_MAX_LENGTH = 250

MAX_COOKING_TIME = 60 * 24 * 7

INGREDIENT_NAME_MAX_LENGTH = 64
INGREDIENT_MEASUREMENT_UNIT_MAX_LENGTH = 32

TAG_NAME_MAX_LENGTH = 32
RECIPE_NAME_MAX_LENGTH = 200


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}

SWAGGER_SETTINGS = {
    'sheme': 'bearer',
    "bearerFormat": 'JWT',
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = env('TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = env('USE_TZ') == 'True'


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'collected_static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'backend_static' / 'static' / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

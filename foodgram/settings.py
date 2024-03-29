import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = Path(BASE_DIR, '.env')
if dotenv_path.is_file():
    load_dotenv(dotenv_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foorgram.settings")

SECRET_KEY = os.getenv('DJANGO_KEY')

DEBUG = bool(os.getenv('DJANGO_DEBUG') == 'True')

EMAIL = bool(os.getenv('DJANGO_EMAIL') == 'True')

LOCAL = bool(os.getenv('LOCAL_WORK') == 'True')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    'testserver',
]

INSTALLED_APPS = [
    'users',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',
    'api',
    'about',
    'recipes',
]

if DEBUG and LOCAL:
    INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG and LOCAL:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = 'foodgram.urls'

TEMPLATES_DIR = Path(BASE_DIR, "templates")
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'recipes.context_processors.tags',
                'recipes.context_processors.purchases_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodgram.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db_from_postgres.sqlite3',
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa: E501
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = Path(BASE_DIR, 'static')
STATICFILES_DIRS = (
    Path(BASE_DIR, 'assets'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = Path(BASE_DIR, 'media')

LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "recipes:index"

# Движок email. filebased - для тестирования, smtp - для отправки.
if EMAIL:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

# Папка, в которую будут складываться файлы писем
EMAIL_FILE_PATH = Path(BASE_DIR, "sent_emails")

DEFAULT_FROM_EMAIL = 'foodgram-noreply@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'knoort1@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('GOOGLE_PASSWD')
EMAIL_USE_TLS = True

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}
if LOCAL:
    SITE_ID = 3
else:
    SITE_ID = 1

PAGINATION_PAGE_SIZE = 6
PREVIEWS_COUNT = 3

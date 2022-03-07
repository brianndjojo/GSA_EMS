"""
Django settings for gsaEMS project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import environ

env = environ.Env(Debug=(bool, False))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Path for Environ to encrypt secret key
BASE_DIR2 = Path(__file__).resolve().parent
# Take environment variables from .env file

#READ_DOT_ENV_FILE = env.bool('READ_DOT_ENV_FILE', default=False)
#if READ_DOT_ENV_FILE:
#    environ.Env.read_env(os.path.join(BASE_DIR2, '.env'))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR2, '.env'))
# False if not in os.environ because of casting above
DEBUG = env('DEBUG')

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')




ALLOWED_HOSTS = []

GOOGLE_MAPS_API_KEY = 'AIzaSyDvhBmLgo9qIYMKf5aLElPHt8wEcITWXiE'

# Application definition

# To improve Security: 
# https://opensource.com/article/18/1/10-tips-making-django-admin-more-secure
# https://hackernoon.com/5-ways-to-make-django-admin-safer-eb7753698ac8

# To check whether the website is secure enough: https://djcheckup.com/

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #third-party apps
    # REST framwork for powerful and flexible toolkit for building Web APIs
    'rest_framework',
    'crispy_forms',
    'crispy_tailwind',
    #FOR SECURITY
    #https://github.com/dmpayton/django-admin-honeypot
    'admin_honeypot',
    
   
  

    #local apps
    'users',
    'events',
    'venues'
    
]

#https://github.com/django-crispy-forms/crispy-tailwind
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

# Calendarium
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.template.context_processors.request',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'gsaEMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates" / "html"],
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

WSGI_APPLICATION = 'gsaEMS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env("DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = 'templates/static/'

# Specifies the directory for Static Files.
STATICFILES_DIRS = [
    BASE_DIR / "templates" / "static",
    BASE_DIR / "templates" / "static" / "css",
    BASE_DIR / "templates" / "static" / "js",
]


STATIC_ROOT = "static_root"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Informs Django which apps have customized user-models..
AUTH_USER_MODEL = 'users.User'

# Email backend specifies all the settings when Django sends emails.
# By default EMAIL_BACKEND uses SMTP, console used for testing offline.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# To specify what page to redirect to when login is successful.
LOGIN_REDIRECT_URL = "/"

LOGIN_URL = "/login"

LOGOUT_REDIRECT_URL = LOGIN_URL

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = "DENY"

    ALLOWED_HOSTS = ['gsa-ems-ot87b.ondigitalocean.app']

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = True
    EMAIL_PORT = env("EMAIL_PORT")
    DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
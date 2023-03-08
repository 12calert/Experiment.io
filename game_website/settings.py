"""
Django settings for game_website project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1u6r1oki8pk9=g)&x%_7glcn-ja^@@o&ggordj0$krek-5y0ye'

# NEEDED FOR PRODUCTION
DEFAULT_AUTO_FIELD='django.db.models.AutoField'  

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For Render hosting
]

ROOT_URLCONF = 'game_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'game_website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

#getting errors so changed this for now
DATABASES ={}
"""DATABASES = {

    'default': dj_database_url.config(default='postgres://map_game_898y_user:PRnhM14xT9oTFNiW4I2p1cfaSB5ajxjj@dpg-cfr4u2un6mpirvus1vt0-a.frankfurt-postgres.render.com/map_game_898y')
}"""
DATABASES['default'] = dj_database_url.parse('postgres://map_game_us3g_user:v2eGa2v12vF9LAcGR1zdNXgBnOwC8iR2@dpg-cg2ep682qv24hdl42pb0-a.frankfurt-postgres.render.com/map_game_us3g', conn_max_age=600)

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': 'mydatabase', # This is where you put the name of the db file. 
#                 # If one doesn't exist, it will be created at migration time.
#    }
#}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join('assets'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # for Render hosting
LOGIN_REDIRECT_URL = 'home' # page which shows after login (researcher view)
LOGOUT_REDIRECT_URL = 'home' # page which shows after logout
LOGIN_URL = "researcher_login"
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')


ASGI_APPLICATION = "game_website.asgi.application"

#Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("rediss://red-cfkcs79a6gductmeqb10:6rIh0otNtRwUTuuyI7jKgMuOYmWQi4xY@frankfurt-redis.render.com:6379")],
        },
    },
}
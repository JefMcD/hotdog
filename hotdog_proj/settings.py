"""
Django settings for hotdog_proj project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# https://docs.djangoproject.com/en/1.11/ref/settings/#media-root
# Absolute filesystem path to the directory that will hold user-uploaded files.
# MEDIA_ROOT = os.path.join(BASE_DIR,'static/network/users')
MEDIA_ROOT =  os.path.join(BASE_DIR, 'hotdog_app_media')
MEDIA_URL = '/hotdog_app_media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'jeffers.pythonanywhere.com',
    'localhost:5173/',
    '127.0.0.1',
]


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic', 
    'hotdog_app',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hotdog_proj.urls'

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

WSGI_APPLICATION = 'hotdog_proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': config('MYSQL_hotdog_DB'),
        'USER': config('MYSQL_USERNAME'),
        'PASSWORD': config('MYSQL_PASSWORD'),
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'OPTIONS': {
            'read_default_file': '/etc/mysql/my.cnf',
        },
    }
}
'''

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Define Custom User Model
AUTH_USER_MODEL = "hotdog_app.User" # Abstract User model

# Default path when User tries to access site when not logged in
LOGIN_URL = '/login'
#AUTH_USER_MODEL = "hungry_hippo_app.User"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIR = [
     os.path.join(BASE_DIR, 'hotdog_app/static/react_frontend'), 
] #Additional paths to be handled by static data

# must be called 'staticfiles' for whitenoise to work
STATIC_ROOT =  os.path.join(BASE_DIR, 'staticfiles') 

#File storage engine used by collectstatic. 
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'


INTERNAL_IPS = [
   '127.0.0.1',  # example IP, add your own IPs here
   # ...
]



CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # React Client Netlify/Vercel domain Note No trailing slash 'http://localhost:5173/'
]

# Optionally, to allow all origins:
CORS_ALLOW_ALL_ORIGINS = True





CSRF_COOKIE_SECURE = True 

# Add the CSRF domains here
CSRF_TRUSTED_ORIGINS = [ 
    'http://jeffers.pythonanywhere.com',
    'http://localhost:5173/', # seperate local server used for React Client eg Vercel/Netlify
    'http://127.0.0.1',
] 

FILE_UPLOAD_PERMISSIONS = 644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 730
SESSION_COOKIE_SECURE =True

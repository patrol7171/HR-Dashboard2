"""
Django settings for hr_dashboard2 project.

Generated by 'django-admin startproject' using Django 2.2.2.

"""

import os
import django_heroku
import dotenv



# Environment paths 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# *** Use .env locally only ***
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ADMIN_PSWD = os.environ.get('ADMIN_PSWD')
    GEOCODIO_API_KEY = os.environ.get('GEOCODIO_API_KEY')
    MAPBOX_API_KEY = os.environ.get('MAPBOX_API_KEY')
    from config import DATABASES
else: # *** For Heroku only *** 
    SECRET_KEY = os.environ.get('App-Secret-Key')
    ADMIN_PSWD = os.environ.get('Admin-Pswd')
    GEOCODIO_API_KEY = os.environ.get('Geocodio-API-Key')
    MAPBOX_API_KEY = os.environ.get('Mapbox-API-Key')
    MYSQLDB_PSWD = os.environ.get('Gearhost-MySQL-Pswd')
    PGSQL_PSWD = os.environ.get('Elephant-SQL-Pswd')
    DATABASES = {
        'default': {
            'ENGINE':'django.db.backends.mysql',
            'NAME':'hrportal2db',                  
            'USER':'hrportal2db',
            'PASSWORD':MYSQLDB_PSWD,
            'HOST':'den1.mysql1.gear.host',
            'PORT':'3306',
        },
        'hr_data': {
            'ENGINE':'django.db.backends.postgresql',
            'NAME':'ebjjixcv',                  
            'USER':'ebjjixcv',
            'PASSWORD':PGSQL_PSWD,
            'HOST':'ruby.db.elephantsql.com',
            'PORT':'5432',
        }
    }



DEBUG = True

#DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ['hr-portal2.herokuapp.com']

DATABASE_ROUTERS = ['hr_dashboard2.dbrouter.HRDataRouter']



# Application definition
INSTALLED_APPS = [   
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'departments.apps.DepartmentsConfig',
    'crispy_forms', 
]



CRISPY_TEMPLATE_PACK = 'bootstrap4'



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



ROOT_URLCONF = 'hr_dashboard2.urls'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['hr_dashboard2/templates'],
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



WSGI_APPLICATION = 'hr_dashboard2.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static/Media files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



# Authentication and Login info
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

ADMIN_LOGIN = 'admin'
ADMIN_PASSWORD = ADMIN_PSWD

AUTHENTICATION_BACKENDS = [
    'accounts.auth_backends.AuthBackend',
]

AUTH_USER_MODEL = 'accounts.CustomUser'



# Activate Django-Heroku
django_heroku.settings(locals())

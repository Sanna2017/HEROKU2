import os
from google.oauth2 import service_account
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-_vyw6na+6wqn07oqwgcyw87l_g@&jy2#nh1d#+r98a9c7t1!f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['api-house-si.herokuapp.com']
#127.0.0.1  # he had


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'background_task',
    'users',
    'task',
    'house',
    'background_jobs',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'taskful_api.urls'

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

WSGI_APPLICATION = 'taskful_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd5ub5ag6ln9gcc',
        'USER': 'kgwagrclmekybr',
        'PASSWORD': '17e27cf249a9e5c356ffc329e98a181bb10cc97c82f48a7d871b1ff135dbd6a5',
        'HOST': 'ec2-52-48-159-67.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


STATIC_URL = '/static/' #already there
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]  #to check here, not only app level
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') #for Deployment, folder 'staticfiles' will be created on remote server
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#file storage engine used when collecting static files with the collecstatic command

####################################################################################
#The STATICFILES_DIRS setting should not contain the STATIC_ROOT setting
#'static' and 'staticfiles' names have to be different
###################################################################################
""" SOLUTION

if DEBUG:
        STATICFILES_DIRS = [
            os.path.join(BASE_DIR, 'static')
       ]
    else:
        STATIC_ROOT = os.path.join(BASE_DIR, 'static')
        
""" 

#LOCAL MEDIA STORAGE
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#DEPLOYMENT
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'prod_api_bucket'
GS_FILE_OVERWRITE = True
# if we upload a file which has the same name as a file that already exists
# in our bucket at the same location, then we're just going to overwrite 
# that file and we're going to replace it with the file that was just uploaded
GS_CREDENTIALS = service_account.Credentials.from_service_account_file('ornate-bebop-345202-fe900751a7a3.json')


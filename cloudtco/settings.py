import os
gettext = lambda s: s
DATA_DIR = os.path.dirname(os.path.dirname(__file__))
"""
Django settings for cloudtco project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import stripe
import boto3
import logging
# import subprocess

LOG = logging.getLogger(__name__)

AWS_ACCESS_KEY = 'AKIAII45QZAB34UTPY6Q'
AWS_SECRET_KEY = '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'
region = 'ap-northeast-1'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0xiqodf*7e7bpnm0=w1lr7w1jfmzz71vd-wtx+7vov!)$#v&th'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
# TEMPLATE_DEBUG = DEBUG

# TEMPLATE_DIRS = (
#     'C:/Users/Desktop/haareesh/08-11/cloudtco_updated/cloudtco/tcoapp/templates', 
# )

#ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'tcoapp',
    'tco',
    'silver',
    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework.authtoken',
]

SITE_ID = 1

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cloudtco.urls'

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

WSGI_APPLICATION = 'cloudtco.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'updatedtco',
        'USER': 'root',
        'PASSWORD': 'ysec@123',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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



AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',    
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    'django.core.context_processors.request',
   
)

# Sign UP settings
ACCOUNT_EMAIL_REQUIRED = True

# auth and allauth settings
LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'METHOD': 'js_sdk'  # instead of 'oauth2'
    }
}




# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(DATA_DIR, 'static')

MEDIA_ROOT = os.path.join(DATA_DIR, "static/media")
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'tcoapp', 'static'),
)


# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),    
# ]


# REST_FRAMEWORK = {
# 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),

# }

# REST_SESSION_LOGIN = False

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.TokenAuthentication',
#     ),
#    'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.AllowAny',
#     ),
# }



# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#     )
# }



# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.TokenAuthentication',
#     )
# }



#STRIPE TEST KEYS
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_test_dEqr2qk4EqZQnjOI1njj7GWD")
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "pk_test_n1Ak7Xljmf1QFk3NPr8kloSF")

STRIPE_API_KEY = "pk_test_n1Ak7Xljmf1QFk3NPr8kloSF"
stripe.api_key = "sk_test_dEqr2qk4EqZQnjOI1njj7GWD"

# Stripe keys
STRIPE_PUBLISHABLE = 'pk_test_n1Ak7Xljmf1QFk3NPr8kloSF'
STRIPE_SECRET = 'sk_test_dEqr2qk4EqZQnjOI1njj7GWD'

# # STRIPE LIVE KEYS
# STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_live_h9QrrTZkCkOST9Jh8fpAphw5")
# STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", " pk_live_TvdYV9mckJAtAfoRTbVDhdWx")

# STRIPE_API_KEY = "pk_live_TvdYV9mckJAtAfoRTbVDhdWx"
# stripe.api_key = "sk_live_h9QrrTZkCkOST9Jh8fpAphw5"

# STRIPE_PUBLISHABLE = 'pk_live_TvdYV9mckJAtAfoRTbVDhdWx'
# STRIPE_SECRET = 'sk_live_h9QrrTZkCkOST9Jh8fpAphw5'

#email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'vinodsesetti@gmail.com'

EMAIL_HOST_PASSWORD = '8019166677'

EMAIL_PORT = 587
EMAIL_USE_TLS = True

STATICFILES_FINDERS = [
     'django.contrib.staticfiles.finders.FileSystemFinder',
     'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
 ]

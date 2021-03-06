"""
Django settings for clubfinance project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rug!t67jj5dn7oyg5f1_915d)!yja6e$wwh1uw35_naa2aovkc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'users.apps.UsersConfig',
    'membershipfees.apps.MembershipfeesConfig',
    'baton',
    'django.contrib.admin',
    'baton.autodiscover',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'clubfinance.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'clubfinance.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

BATON = {
    'SITE_HEADER': 'Haxkohle',
    'SITE_TITLE': 'Haxkohle',
    'INDEX_TITLE': 'Haxkohle admin',
    'SUPPORT_HREF': 'https://github.com/haxko/haxkohle/issues',
    'COPYRIGHT': '', # noqa
    'POWERED_BY': '<a href="https://haxko.space/">haxko e.V</a>',
    'CONFIRM_UNSAVED_CHANGES': True,
    'SHOW_MULTIPART_UPLOADING': True,
    'ENABLE_IMAGES_PREVIEW': True,
    'CHANGELIST_FILTERS_IN_MODAL': True,
    'MENU_ALWAYS_COLLAPSED': False,
    'MENU_TITLE': 'Menu',
    'MENU':  (
        { 'type': 'title', 'label': 'Members and Authentication', 'default_open': True, 'children': [
            { 'type': 'free', 'label': 'Users', 'url': '/admin/auth/user/' },
            { 'type': 'free', 'label': 'Groups', 'url': '/admin/auth/group/' },
            { 'type': 'free', 'label': 'Subscriptions', 'url': '/admin/users/subscription/' },
        ] },
        { 'type': 'title', 'label': 'Banking', 'default_open': True, 'children': [
            { 'type': 'free', 'label': 'Import Data', 'url': '/finance/admin/import_camt/' },
            { 'type': 'free', 'label': 'Match Transactions', 'url': '/finance/admin/match_transactions/' },
            { 'type': 'free', 'label': 'Bank Accounts', 'url': '/admin/membershipfees/bankaccount/' },
            { 'type': 'free', 'label': 'Bank Transfers', 'url': '/admin/membershipfees/banktransaction/' },
        ] },
    ),

}



CRISPY_TEMPLATE_PACK = 'bootstrap4'
CAMT_UPLOAD_PASS='0a887e543f16cd2e9ae663c88ef9c8c5cc587569a897b6b53b256fa1'
DEFAULT_MONTLY_FEE=20
DEFAULT_CURRENCY="EUR"
MEMBERSHIP_NUMBER_LABEL="Owl number"

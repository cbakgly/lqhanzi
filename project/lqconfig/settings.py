# -*- coding:utf8 -*-
"""
Django settings for lqconfig project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
SECRET_KEY = 'nej4uf&$0-18*bb)--qjx3vc6-ahsxt!c!z92g^h$qjl4036*x'

DEBUG = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ["*", ]

ROOT_URLCONF = 'lqconfig.urls'
WSGI_APPLICATION = 'lqconfig.wsgi.application'
AUTH_USER_MODEL = 'backend.User'

# For customized user model, guardian must be tuned
# GUARDIAN_MONKEY_PATCH = False
# INTERNAL_IPS = ('127.0.0.1',)
ADMINS = [('Xiandu', 'lqs.xiandu@qq.com'), ('cbakgly', 'cbakgly@qq.com')]
MANAGERS = [('Xiandu', 'lqs.xiandu@qq.com'), ('cbakgly', 'cbakgly@qq.com')]
SERVER_EMAIL = 'root@hanzi.lqdzj.cn'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True

USE_S3_HANZI_PICTURE = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/')]
STATIC_ROOT = os.path.join(BASE_DIR, 'allstatic/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/uploads/')

# Registration Settings
ACCOUNT_ACTIVATION_DAYS = 3
REGISTRATION_OPEN = True
REGISTRATION_AUTO_LOGIN = True
LOGIN_REDIRECT_URL = '/workbench/'
REGISTRATION_EMAIL_SUBJECT_PREFIX = '[Please verify your email account for lqhanzi.]'
SEND_ACTIVATION_EMAIL = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'alqdzj@126.com'  # 账号密码同aws密码
EMAIL_HOST_PASSWORD = 'dongpeilou404'
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL
EMAIL_HOST = 'smtp.126.com'
EMAIL_PORT = 25
# Registration Settings end

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SECURE_REDIRECT_EXEMPT = ['index', 'stroke_', 'inverse_', 'variant_', 'dicts\/', '']
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

CACHE_MIDDLEWARE_SECONDS = 10
# APPEND_SLASH = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_filters',
    'rest_framework',
    # 'guardian',
    # 'debug_toolbar',
    'registration',
    'hanzi',
    'sysadmin',
    'workbench',
    'backend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'backend.context_processors.today_credits',
                'backend.context_processors.model_enum',
                'backend.context_processors.lqhanzi_font',
            ],
        },
    },
]

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8, }},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'guardian.backends.ObjectPermissionBackend'
)

# Rest framework paging setting added by @xianduan
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'PAGE_SIZE': 10,
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1'],
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.DjangoFilterBackend',
    ),
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'lqhanzi',
        'OPTIONS': {
            'MAX_ENTRIES': 500
        },
    },
}

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lqhanzi',
        'USER': 'lq',
        'PASSWORD': '123456',
        'HOST': '192.168.16.3',
        # 'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4', 'init_command': 'SET default_storage_engine=InnoDB'},
    }
}
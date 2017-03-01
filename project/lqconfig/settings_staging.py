# -*- coding:utf8 -*-
"""
Specific Django settings for staging test
"""

# flake8: noqa

from settings import *

# Customized staging MySQL setup
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lqhanzi',
        'USER': 'root',
        'PASSWORD': 'mymysqlpassword',
        'HOST': 'db',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4', 'init_command': 'SET default_storage_engine=InnoDB'}
    }
}

INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

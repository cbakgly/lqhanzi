# -*- coding:utf8 -*-

from settings import *

DEBUG = False
CACHE_MIDDLEWARE_SECONDS = 60

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

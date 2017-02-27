# -*- coding:utf8 -*-
"""
Specific Django settings for CI test
"""

# flake8: noqa

import os
from settings import *

# use sqlite for CI test
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# disable cache for CI test
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}

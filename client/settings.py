# Default Settings

import os

PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])

TEMP_DIR = os.path.join(PROJECT_PATH, '..', 'tmp',)

API_USER = ''  # Set Me
API_PASS = ''  # Set Me
API_HOST = ''  # Set Me

DEBUG = False

# NB It's a better idea to put your settings in a local_settings.py overrides file.
try:
    from local_settings import *
except ImportError:
    pass

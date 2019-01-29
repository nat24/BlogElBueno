from .base import *
import os

SECRET_KEY = os.getenv('SECRET_KEY',None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG',False)

ALLOWED_HOSTS = [os.getenv('HOSTS',False)]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':   os.getenv('DBNAME',None),                      
        'USER': os.getenv('DBUSER',None),
        'PASSWORD': os.getenv('DBPASS',None),
        'HOST': os.getenv('DBHOST',None),
        'PORT': 5432',
    }
}



STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
"""
Django settings for echo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from project_runpy import env


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

SECRET_KEY = env.get('SECRET_KEY', '123456')

DEBUG = env.get('DEBUG', False)

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'echo.urls'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'echo'),
)


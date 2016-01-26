# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pf-@jxtojga)z+4s*uwbgjrq$aep62-thd0q7f&o77xtpka!_m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'guestbook'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# When 'NODB' is enabled,we skip Database and Cache setup. This is useful
# to test the rest of the Django deployment while boostrapping the application.
if os.getenv('NODB'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    # Dockerfile reads the DJANGO_PW from the secret into an environment
    # variable but its not there on kubectl exec. Soon Kubernetes versions
    # will have secrets as environment variables but currently just read it
    # from the volume
    DJANGO_PW = os.getenv('DJANGO_PASSWORD')
    if not DJANGO_PW:
        try:
            f = open('/etc/secrets/djangouserpw')
            DJANGO_PW = f.readline().rstrip()
        except IOError:
            pass
    if not DJANGO_PW:
        raise Exception("No DJANGO_PASSWORD provided.")

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'guestbook',
            'USER': 'django_user',
            'PASSWORD': DJANGO_PW,
            'HOST': os.getenv('POSTGRES_SERVICE_HOST', '127.0.0.1'),
            'PORT': os.getenv('POSTGRES_SERVICE_PORT', 5432)
        }
    }

    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': [
                '%s:%s' % (os.getenv('REDIS_MASTER_SERVICE_HOST', '127.0.0.1'),
                           os.getenv('REDIS_MASTER_SERVICE_PORT', 6379)),
                '%s:%s' % (os.getenv('REDIS_SLAVE_SERVICE_HOST', '127.0.0.1'),
                           os.getenv('REDIS_SLAVE_SERVICE_PORT', 6379))
            ],
            'OPTIONS': {
                'PARSER_CLASS': 'redis.connection.HiredisParser',
                'PICKLE_VERSION': 2,
                'MASTER_CACHE': '%s:%s' % (
                    os.getenv('REDIS_MASTER_SERVICE_HOST', '127.0.0.1')
                    , os.getenv('REDIS_MASTER_SERVICE_PORT', 6379))
            },
        },
    }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
# STATIC_URL = 'https://storage.googleapis.com/delete-me-1156/static/'

STATIC_ROOT = 'static/'

from pathlib import Path
import os, environ
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = 'django-insecure-3c_6wd)nft0nm#g(p-*3cjiu_#=gr+^#8y%rjhwb4dy$v-jpd_'

# DEBUG = True
# DEBUG = env('DEBUG')
# ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')

ALLOWED_HOSTS=['*','192.168.43.185','127.0.0.1','localhost','demo-contactx.herokuapp.com']
DEBUG = True

# Application definition

INSTALLED_APPS = [
  'channels',
  'phonenumber_field',

  'account',
  'contacts',

  'rest_framework',
  'corsheaders',
  'rest_framework.authtoken',
  
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',    
  'django.contrib.postgres',
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'demoserver.urls'

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


WSGI_APPLICATION = 'demoserver.wsgi.application'
ASGI_APPLICATION = 'demoserver.routing.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Tells django to use the custom user model we've creating in the accounts app
AUTH_USER_MODEL = "account.Account"

# Settings for the django rest framework 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


CHANNEL_LAYERS = {
    "default": {        
        "BACKEND": 'channels_redis.demoserver.RedisChannelLayer',
        'CONFIG': {
            # "hosts": ["redis://redis:6379/0",]
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}
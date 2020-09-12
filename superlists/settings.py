import os
from secrets.secrets import ReturnSecretKey

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

secret_key_finder = ReturnSecretKey()
SECRET_KEY = secret_key_finder.return_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!

if 'DJANGO_DEBUG_FALSE' in os.environ:
	DEBUG = False
	SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
	ALLOWED_HOSTS = ['www.thetodolistsite.com', 'localhost']

else:
	DEBUG = True
	SECRET_KEY = 'insecure_key_for_dev'
	ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lists',
    'accounts',
]

AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = [

'accounts.authentication.PasswordlessAuthenticationBackend',

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

ROOT_URLCONF = 'superlists.urls'

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

WSGI_APPLICATION = 'superlists.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'handlers': {
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',	
		},
	},
	'loggers': {
		'django': {
			'handlers': ['console'],
		},
	},
	'root': {'level': 'INFO'},
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'onlyforbook61@gmail.com'
EMAIL_HOST_PASSWORD = 'loopwake'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

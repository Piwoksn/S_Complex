from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-77*%9t#4u60h2=)pe4&lm+gqg@vhf=r((l3du!e=4q3gh%4b+%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['myshopcomplex.com',
#                  'a961-197-210-78-239.ngrok.io', 'localhost']

# My Abstract User
AUTH_USER_MODEL = 'myapp.User'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 3rd Party
    'allauth',
    'allauth.account',
    'crispy_forms',
    'crispy_bootstrap5',
    'rest_framework',
    # 'paypal.standard.ipn',
    
    # local apps
    'subscription',
    'myapp',
    'shopapp',
    'chats',
    'api',
]

ALLOWED_CRISPY_TEMPLATE_PACKS = ['bootstrap5',]
CRISPY_TEMPLATE_PACK = 'bootstrap5'




MIDDLEWARE = [
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Shop.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
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

WSGI_APPLICATION = 'Shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Africa/Lagos'


USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# My Images URL

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# PAYSTACK

PAYSTACK_SECRET_KEY = 'sk_live_47aea5336926896f66159a39039156a66ebcb4d6'
PAYSTACK_PUBLIC_KEY = 'pk_live_0b4a43086e3a515fbbd7d3490c12d5e0631b730f'

# # PAYPAL
PAYPAL_CLIENT_ID = 'AfiKbSHcoiYodXw8_7vF3GYoMmenhRB10XFaHV8d-SQszmONRpOXc0_JSl7cUYRtjlL6AnuaLQsoRvXA'
PAYPAL_CLIENT_SECRET = 'EHxPp56V1hqsEZBCYlz6rij4HPjVUlFLaVKfEAeTQ77f2KMrduxt2JXrOgKktD-5As-IynCzfS414cCt'

PAYPAL_TEST = True
# ____________________________

# For My Images
MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')


# -----------------My cart-----------------

# Enable sessions
# Database-backed sessions (default)
SESSION_ENGINE = "django.contrib.sessions.backends.db"
# or
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"  # Caching sessions
# Set a session key prefix to avoid conflicts
SESSION_COOKIE_NAME = 'shopping_cart_session'


# -----------------End cart-----------------


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# ----------------------------------------------------------------------
# SMTP Configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'piwoksn@gmail.com'
EMAIL_HOST_PASSWORD = 'dzrb qnun nley xbqf'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'piwoksn@gmail.com'
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # or "optional" if you want users to skip it
ACCOUNT_CONFIRM_EMAIL_ON_GET = True       # Optional: activates on link click, no button

AUTHENTICATION_BACKENDS =[
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

ACCOUNT_LOGOUT_REDIRECT = 'home'
LOGIN_REDIRECT_URL = 'portal'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
# ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*']



# ----------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        # You can set the level to your preferred log level (e.g., DEBUG, INFO, WARNING)
        'level': 'DEBUG',
    },
}

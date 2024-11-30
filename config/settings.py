from pathlib import Path
from environs import Env
import os
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

# get .env if exists (for environments variables)
env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.



                                            # PRODUCTION mode
# ---------------------------------------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ---------------------------------------------------------------------------------
                                            # DEVELOP mode MEHRAN TARIF
# ---------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent











                                            # PRODUCTION mode
# ---------------------------------------------------------------------------------
# DEBUG = False
                                            # DEVELOP Mode
# ---------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG")








                                            # PRODUCTION mode
# ---------------------------------------------------------------------------------
# SECRET_KEY = "alskdjhfjkdlksdfksdfoiwijwemcv51234SzX3!2x^5!4GcH6$2FvBhJ7%$-3uxa2g7q)w^5vwgoem@28m$__4wii4$uxee5x74zk8*jd1ifle"
                                            # DEVELOP Mode
# ---------------------------------------------------------------------------------
SECRET_KEY = env("DJANGO_SECRET_KEY")






# Allowed hosts
                                            # PRODUCTION mode
# ---------------------------------------------------------------------------------
# ALLOWED_HOSTS = []
                                            # DEVELOP Mode
# ---------------------------------------------------------------------------------
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")








# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "crispy_bootstrap4",
    "allauth",
    "allauth.account",
    "rosetta",
    "accounts.apps.AccountsConfig",
    "pages.apps.PagesConfig",
    "products.apps.ProductsConfig",
    "cart.apps.CartConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "config.urls"


BASE_DIR_2 = Path(__file__).resolve().parent.parent
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR_2.joinpath("templates"))],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Custom Context processors
                "cart.context_processors.cart",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"





                                            # PRODUCTION mode
# ---------------------------------------------------------------------------------
# DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}
                                            # DEVELOP mode
# ---------------------------------------------------------------------------------
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv("POSTGRES_DB"),
#         "USER": os.getenv("POSTGRES_USER"),
#         "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
#         "HOST": os.getenv("POSTGRES_HOST"),
#         "PORT": os.getenv("POSTGRES_PORT"),
#     }
# }
# ---------------------------------------------------------------------------------
                                            # DEVELOP mode MEHRAN TARIF
# ---------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}





# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "fa-ir"
# LANGUAGE_CODE = "en"
LANGUAGES = (
    ("en", "English"),
    ("de", "German"),
    ("fa", "Persian"),
)

TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")





DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"





# accounts config
AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"





# CRISPY_TEMPLATE_PACK
CRISPY_TEMPLATE_PACK = "bootstrap4"

# For allauth Package
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

                                            # PRODUCTION mode
# ---------------------------------------------------------------------------------
# EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
                                            # DEVELOP mode
# ---------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"




EMAIL_HOST="smtp.c1.liara.email"
DEFAULT_FROM_EMAIL="info@acronproject.com"
EMAIL_PORT=587
EMAIL_HOST_USER="angry_saha_23h3mb"
EMAIL_HOST_PASSWORD="84fe9e5e-64c1-497a-80d9-0dd550d008d3"
EMAIL_USE_TLS=True





ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True


CSRF_TRUSTED_ORIGINS = [
    "http://www.acronproject.com",
    "https://www.acronproject.com",
]


from django.contrib.messages import constants as messages_constants

# For messages framework
MESSAGE_TAGS = {
    messages_constants.ERROR: "danger",
}

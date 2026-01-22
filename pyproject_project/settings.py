from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-=w)otrq$2uku-2#@_ez-!33xt!=^q=#(dgrua__5k$(^j1-kjd"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "social_django",
    "website.apps.WebsiteConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pyproject_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "website.context_processors.google_profile_picture",
            ],
        },
    },
]

WSGI_APPLICATION = "pyproject_project.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    "main": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "main.db",
    },
}

DATABASE_ROUTERS = ["website.db_router.MainRouter"]

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

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kuala_Lumpur"
USE_I18N = True
USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",  # Google
    "django.contrib.auth.backends.ModelBackend",  # normal Django auth
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = (
    "496461563970-jltkj3brmut9ubdcmu7c2fde885ashf0.apps.googleusercontent.com"
)

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ["uitm.edu.my", "student.uitm.edu.my"]


SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = (
    "http://127.0.0.1:8000/oauth/complete/google-oauth2/"
)

SOCIAL_AUTH_GOOGLE_OAUTH2_AUTHORIZATION_URL = (
    "https://accounts.google.com/o/oauth2/auth"
)
SOCIAL_AUTH_GOOGLE_OAUTH2_TOKEN_URL = "https://oauth2.googleapis.com/token"

SOCIAL_AUTH_LOGIN_ERROR_URL = "/"
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/"
SOCIAL_AUTH_USE_NEXT = True


SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]

SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = [
    "sub",
    "email",
    "name",
    "given_name",
    "family_name",
    "picture",
    "locale",
    "hd",
]

LOGIN_URL = "/oauth/login/google-oauth2/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGOUT_URL = "/accounts/logout/"

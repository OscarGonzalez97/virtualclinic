import os

from virtualclinic.settings import BASE_DIR
from django.core.management.utils import get_random_secret_key

trusted_origins = os.environ.get("CSRF_TRUSTED_ORIGINS")
if trusted_origins is not None:
    CSRF_TRUSTED_ORIGINS = [x.strip() for x in trusted_origins.split(",")]

allowed_hosts = os.environ.get("ALLOWED_HOSTS")
if allowed_hosts is not None:
    ALLOWED_HOSTS = [x.strip() for x in allowed_hosts.split(",")]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = []
DEBUG = False
SECRET_KEY = get_random_secret_key()
# SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 60
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'data/db.sqlite3',
    }
}

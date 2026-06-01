"""Settings del progetto di esempio per django-agesci-theme."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "dev-only-change-me"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # tema AGESCI
    "agesci_theme",
    # Icone Bootstrap (opzionale in produzione; qui abilitato per il demo).
    # In un progetto reale: uv add "django-agesci-campania-theme[icons]"
    "django_bootstrap_icons",
    # app locale
    "app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "app" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # context processor del tema
                "agesci_theme.context_processors.agesci_theme",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "it-it"
TIME_ZONE = "Europe/Rome"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================================================
#  Personalizzazione tema AGESCI - cambia qui per provare!
# =========================================================
AGESCI_THEME_BRANCA = "eg"          # generico | capi | lc | eg | rs
AGESCI_THEME_NOME = "Demo AGESCI Campania"
AGESCI_THEME_NAVBAR_TESTO_SCURO = False

# =========================================================
#  Icone Bootstrap — cache consigliata per le prestazioni.
#  Evita di scaricare i SVG da GitHub a ogni richiesta.
#  In produzione: BASE_DIR / ".bs-icons-cache" (fuori da STATIC_ROOT).
# =========================================================
BS_ICONS_CACHE = BASE_DIR / ".bs-icons-cache"

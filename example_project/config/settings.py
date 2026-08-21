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
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # tema AGESCI — DEVE precedere le app allauth in INSTALLED_APPS: il
    # loader APP_DIRS di Django scorre le app nell'ordine di INSTALLED_APPS,
    # e i template agesci_theme/templates/allauth/... devono essere trovati
    # PRIMA dei template bundle di allauth stesso per fare da override.
    "agesci_theme",
    # django-allauth (opzionale in produzione; qui abilitato per il demo
    # dell'integrazione Bootstrap — vedi docs/allauth.md).
    # In un progetto reale: uv add "django-agesci-campania-theme[allauth]"
    "allauth",
    "allauth.account",
    "allauth.mfa",
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
    "allauth.account.middleware.AccountMiddleware",
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
#  django-allauth (demo) — vedi docs/allauth.md
# =========================================================
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "optional"    # evita di richiedere SMTP per provare in locale
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
LOGIN_REDIRECT_URL = "/"

# Renderer Bootstrap 5 del tema — attivazione esplicita e opt-in.
# Vedi docs/forms.md per cosa cambia e perché non è automatico.
FORM_RENDERER = "agesci_theme.forms.AgesciFormRenderer"

# =========================================================
#  Personalizzazione tema AGESCI - cambia qui per provare!
# =========================================================
AGESCI_THEME_BRANCA = "generico"    # generico | capi | lc | eg | rs
AGESCI_THEME_NOME = "Demo AGESCI Campania"
AGESCI_THEME_NAVBAR_TESTO_SCURO = False

# =========================================================
#  Icone Bootstrap — cache consigliata per le prestazioni.
#  Evita di scaricare i SVG da GitHub a ogni richiesta.
#  In produzione: BASE_DIR / ".bs-icons-cache" (fuori da STATIC_ROOT).
# =========================================================
BS_ICONS_CACHE = BASE_DIR / ".bs-icons-cache"

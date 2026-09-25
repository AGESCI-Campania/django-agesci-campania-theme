"""Settings del progetto di esempio con il tema CoreUI.

Stesso progetto di settings.py, ma con l'app ``agesci_coreui`` e i template
di app/templates_coreui/ (che estendono ``agesci_coreui/base.html``) cercati
PRIMA di app/templates/. Avvio:

    uv run python example_project/manage.py runserver --settings=config.settings_coreui
"""
from .settings import *  # noqa: F401,F403
from .settings import BASE_DIR, INSTALLED_APPS, TEMPLATES

# agesci_coreui prima di agesci_theme: stesso criterio di APP_DIRS
# documentato in settings.py per allauth.
INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.insert(INSTALLED_APPS.index("agesci_theme"), "agesci_coreui")

TEMPLATES = [dict(TEMPLATES[0])]
TEMPLATES[0]["DIRS"] = [
    BASE_DIR / "app" / "templates_coreui",
    BASE_DIR / "app" / "templates",
]

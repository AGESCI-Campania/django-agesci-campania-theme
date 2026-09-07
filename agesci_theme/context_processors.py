"""Context processor: espone le impostazioni del tema a tutti i template.

Aggiungere in settings.py:

    TEMPLATES = [{
        ...
        "OPTIONS": {
            "context_processors": [
                ...
                "agesci_theme.context_processors.agesci_theme",
            ],
        },
    }]
"""
from django.conf import settings

# Branche valide (devono corrispondere a [data-branca] in _branche.scss)
BRANCHE_VALIDE = {"generico", "capi", "lc", "eg", "rs", "viola", "generico2"}

DEFAULTS = {
    "AGESCI_THEME_BRANCA": "generico",
    "AGESCI_THEME_NOME": "AGESCI Campania",
    # path relativi a STATIC, sovrascrivibili da settings del progetto
    "AGESCI_THEME_LOGO": "agesci_theme/img/agescicam-logo-black.svg",
    "AGESCI_THEME_LOGO_NAVBAR": "agesci_theme/img/EMBLEMA_CAMPANIA_WHITE.svg",
    "AGESCI_THEME_EMBLEMA": "agesci_theme/img/emblemi/EMBLEMA_CAMPANIA.png",
    "AGESCI_THEME_FAVICON_32": "agesci_theme/img/favicon/favicon32x32.png",
    "AGESCI_THEME_FAVICON_16": "agesci_theme/img/favicon/favicon16x16.png",
    # navbar scura quando la branca ha colore chiaro (es. LC giallo)
    "AGESCI_THEME_NAVBAR_TESTO_SCURO": False,
}


def agesci_theme(request):
    branca = getattr(settings, "AGESCI_THEME_BRANCA", DEFAULTS["AGESCI_THEME_BRANCA"])
    if branca not in BRANCHE_VALIDE:
        branca = DEFAULTS["AGESCI_THEME_BRANCA"]

    ctx = {key.lower(): getattr(settings, key, default) for key, default in DEFAULTS.items()}
    ctx["agesci_theme_branca"] = branca
    return ctx

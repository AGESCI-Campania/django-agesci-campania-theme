"""System check del tema CoreUI (``manage.py check``)."""
from django.apps import apps
from django.core import checks


@checks.register(checks.Tags.templates)
def agesci_theme_installato(app_configs, **kwargs):
    """Il tema CoreUI usa dal tema base template tag (``agesci_tags``,
    ``agesci_components``), context processor e immagini: senza
    ``agesci_theme`` in ``INSTALLED_APPS`` mancano."""
    if apps.is_installed("agesci_theme"):
        return []
    return [
        checks.Error(
            "agesci_coreui richiede anche 'agesci_theme' in INSTALLED_APPS.",
            hint='Aggiungi "agesci_theme" subito dopo "agesci_coreui".',
            id="agesci_coreui.E001",
        )
    ]


@checks.register(checks.Tags.templates)
def agesci_coreui_prima_del_tema(app_configs, **kwargs):
    """``agesci_coreui`` deve precedere ``agesci_theme``: i template dei
    componenti, dei form e di allauth che differiscono (markup Bootstrap 5
    invece di Bootstrap 6) sono copie con lo stesso percorso di quelli del
    tema base, e il loader ``APP_DIRS`` usa il primo trovato. Nell'ordine
    sbagliato non c'è errore: le pagine escono con il markup sbagliato."""
    nomi = [c.name for c in apps.get_app_configs()]
    if "agesci_theme" not in nomi or nomi.index("agesci_coreui") < nomi.index("agesci_theme"):
        return []
    return [
        checks.Error(
            "'agesci_coreui' deve precedere 'agesci_theme' in INSTALLED_APPS.",
            hint="I template CoreUI sovrascrivono quelli del tema base solo se "
            "l'app viene prima nell'ordine di APP_DIRS.",
            id="agesci_coreui.E002",
        )
    ]

"""System check del tema CoreUI (``manage.py check``)."""
from django.apps import apps
from django.core import checks


@checks.register(checks.Tags.templates)
def agesci_theme_installato(app_configs, **kwargs):
    """Il tema CoreUI estende il tema base: senza ``agesci_theme`` in
    ``INSTALLED_APPS`` mancano template tag (``agesci_tags``,
    ``agesci_components``), immagini, override di allauth e form."""
    if apps.is_installed("agesci_theme"):
        return []
    return [
        checks.Error(
            "agesci_coreui richiede anche 'agesci_theme' in INSTALLED_APPS.",
            hint='Aggiungi "agesci_theme" subito dopo "agesci_coreui".',
            id="agesci_coreui.E001",
        )
    ]

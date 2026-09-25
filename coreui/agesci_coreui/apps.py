from django.apps import AppConfig


class AgesciCoreuiConfig(AppConfig):
    name = "agesci_coreui"
    verbose_name = "AGESCI Campania Theme (CoreUI)"

    def ready(self):
        from . import checks  # noqa: F401  registra i system check

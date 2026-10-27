"""Widget e campi di form basati sui componenti free di CoreUI 5.

Come ``agesci_theme.forms.SelectMultiploADiscesa`` i template stanno in un
namespace proprio (``agesci_coreui/forms/...``), trovato via ``APP_DIRS``
anche dal renderer di default di Django: basta ``agesci_coreui`` in
``INSTALLED_APPS``. Il JS viene da ``coreui.bundle.min.js``, già caricato da
``agesci_coreui/base.html``.
"""
from pathlib import Path

from django import forms
from django.forms.renderers import DjangoTemplates
from django.utils.functional import cached_property

from agesci_theme.forms import DJANGO_FORMS_TEMPLATES_DIR

COREUI_FORMS_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


class AgesciCoreuiFormRenderer(DjangoTemplates):
    """Renderer dei widget di form con il markup Bootstrap 5/CoreUI 5.

    È l'equivalente di ``agesci_theme.forms.AgesciFormRenderer`` per i
    progetti che usano il tema CoreUI: dal tema base 3.0 quest'ultimo
    produce markup Bootstrap 6, incompatibile con CoreUI 5. Va attivato
    nelle settings del progetto (vale per tutti i form Django)::

        FORM_RENDERER = "agesci_coreui.forms.AgesciCoreuiFormRenderer"

    Come per il renderer del tema base, ``DIRS`` ha la precedenza su
    ``APP_DIRS``: i template ``django/forms/...`` del pacchetto vincono
    sempre su quelli di Django; gli include (``agesci_theme/components/...``)
    sono risolti via ``APP_DIRS``, quindi con ``agesci_coreui`` prima di
    ``agesci_theme`` in ``INSTALLED_APPS`` si ottengono le copie CoreUI.
    """

    @cached_property
    def engine(self):
        return self.backend(
            {
                "APP_DIRS": True,
                "DIRS": [COREUI_FORMS_TEMPLATES_DIR, DJANGO_FORMS_TEMPLATES_DIR],
                "NAME": "agescicoreuiforms",
                "OPTIONS": {},
            }
        )


class InputChip(forms.Widget):
    """Campo di testo che trasforma ogni voce in un chip (componente
    ``chip-input`` di CoreUI): Invio o il separatore creano il chip,
    Backspace o la "x" lo rimuovono.

    Il JS di CoreUI mantiene un ``<input type="hidden" name="...">`` con i
    valori uniti dal separatore: ``value_from_datadict`` li restituisce come
    lista di stringhe, senza vuoti né spazi ai bordi.

    Uso::

        tag = CampoChip(label="Tag", required=False)
        # oppure, su un campo esistente che accetta una lista:
        tag = forms.Field(widget=InputChip(placeholder="Aggiungi…"))
    """

    template_name = "agesci_coreui/forms/input_chip.html"

    def __init__(self, attrs=None, placeholder="", separator=","):
        super().__init__(attrs)
        self.placeholder = placeholder
        self.separator = separator

    def format_value(self, value):
        if not value:
            return []
        if isinstance(value, str):
            value = value.split(self.separator)
        return [str(v).strip() for v in value if str(v).strip()]

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["placeholder"] = self.placeholder
        context["widget"]["separator"] = self.separator
        return context

    def value_from_datadict(self, data, files, name):
        raw = data.get(name)
        if raw is None:
            return None
        return self.format_value(raw)

    def value_omitted_from_data(self, data, files, name):
        return name not in data


class CampoChip(forms.Field):
    """Campo che restituisce una lista di stringhe, reso con ``InputChip``.

    ``required=True`` richiede almeno un chip. ``max_chip`` (opzionale)
    limita il numero di voci.
    """

    widget = InputChip
    default_error_messages = {
        "max_chip": "Inserisci al massimo %(max)d voci.",
    }

    def __init__(self, *, max_chip=None, **kwargs):
        self.max_chip = max_chip
        super().__init__(**kwargs)

    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, str):
            value = value.split(",")
        return [str(v).strip() for v in value if str(v).strip()]

    def validate(self, value):
        super().validate(value)
        if self.max_chip is not None and len(value) > self.max_chip:
            raise forms.ValidationError(
                self.error_messages["max_chip"], code="max_chip", params={"max": self.max_chip}
            )

"""Renderer di form Bootstrap 5, opt-in per i progetti consumer.

Django non renderizza i widget dei form tramite le ``TEMPLATES`` di
progetto: usa un motore di template separato
(``django.forms.renderers.DjangoTemplates``), la cui ``DIRS`` punta di
default SOLO alla directory dei template di Django stesso. Un override in
``agesci_theme/templates/django/forms/...`` non basta da solo: serve una
sottoclasse che antepone le proprie directory, e il progetto consumer deve
attivarla esplicitamente impostando:

    FORM_RENDERER = "agesci_theme.forms.AgesciFormRenderer"

nelle proprie settings. Non è automatico: vale per TUTTI i form Django del
progetto, non solo per quelli di django-allauth.

Precedenza delle directory: ``DIRS`` è sempre controllata prima di
``APP_DIRS`` (verificato su ``django.template.engine.Engine`` e
``django.template.loaders.filesystem.Loader``: il loader filesystem, con le
directory esplicite di ``DIRS``, viene eseguito prima del loader
app_directories, e restituisce il primo match trovato scorrendo ``DIRS`` in
ordine di lista). Con ``DIRS=[THEME_FORMS_DIR, DJANGO_FORMS_TEMPLATES_DIR]``
questo significa che gli override del tema vincono sempre sui template di
default di Django. ``APP_DIRS=True`` resta attivo come rete di sicurezza per
eventuali altri nomi di template non coperti dal tema, ma NON è un punto di
estensione affidabile per un consumer: mettere un proprio
``templates/django/forms/widgets/attrs.html`` in un'app del progetto non
avrà alcun effetto sui quattro template che il tema già sovrascrive
(``attrs.html``, ``password.html``, ``p.html``,
``errors/list/default.html``), perché ``DIRS`` li trova già prima che
``APP_DIRS`` venga interrogato, indipendentemente dalla posizione dell'app
in ``INSTALLED_APPS``.

Per personalizzare ulteriormente questi template, un consumer deve
sottoclassare ``AgesciFormRenderer`` e anteporre la propria directory a
``engine.dirs`` (letta dinamicamente dal loader ad ogni render, quindi
sicura da modificare dopo l'inizializzazione)::

    from pathlib import Path
    from agesci_theme.forms import AgesciFormRenderer

    class ProgettoFormRenderer(AgesciFormRenderer):
        @cached_property
        def engine(self):
            engine = super().engine
            engine.dirs.insert(0, Path(__file__).resolve().parent / "templates")
            return engine

Il modulo espone anche ``SelectMultiploADiscesa``, un widget
``CheckboxSelectMultiple`` renderizzato come tendina Bootstrap con
checkbox. A differenza degli override sopra, non richiede
``FORM_RENDERER = AgesciFormRenderer``: usa un namespace di template
proprio (``agesci_theme/forms/...``), trovato via ``APP_DIRS`` anche dal
renderer di default di Django — basta ``agesci_theme`` in
``INSTALLED_APPS``. Vedi la classe più sotto e ``docs/forms.md``.
"""

from pathlib import Path

import django.forms.renderers
from django import forms
from django.forms.renderers import DjangoTemplates
from django.utils.functional import cached_property

DJANGO_FORMS_TEMPLATES_DIR = Path(django.forms.renderers.__file__).resolve().parent / "templates"
THEME_FORMS_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


class AgesciFormRenderer(DjangoTemplates):
    """Renderer dei widget di form: applica gli override Bootstrap 5 del
    tema (classi ``form-control``/``form-select``/``is-invalid``, toggle
    mostra/nascondi password, errori come ``invalid-feedback``), poi ricade
    sui template di default di Django per tutto il resto."""

    @cached_property
    def engine(self):
        return self.backend(
            {
                "APP_DIRS": True,
                "DIRS": [THEME_FORMS_TEMPLATES_DIR, DJANGO_FORMS_TEMPLATES_DIR],
                "NAME": "agescitemaforms",
                "OPTIONS": {},
            }
        )


class SelectMultiploADiscesa(forms.CheckboxSelectMultiple):
    """``CheckboxSelectMultiple`` renderizzato come tendina Bootstrap chiusa
    (bottone + menu dropdown con checkbox), non come elenco checkbox aperto.

    A differenza di ``AgesciFormRenderer``, NON richiede
    ``FORM_RENDERER = "agesci_theme.forms.AgesciFormRenderer"``: i suoi
    template vivono in un namespace proprio (``agesci_theme/forms/...``),
    non in ``django/forms/widgets/...``, quindi vengono trovati anche dal
    renderer di default di Django (che ha già ``APP_DIRS=True``) purché
    ``agesci_theme`` sia in ``INSTALLED_APPS`` — requisito già necessario
    per usare il tema. È un widget opt-in per singolo campo: non cambia il
    comportamento delle altre ``CheckboxSelectMultiple`` del progetto.

    Uso::

        interessi = forms.MultipleChoiceField(
            choices=SCELTE,
            required=False,
            widget=SelectMultiploADiscesa(placeholder="Nessuno"),
        )
    """

    template_name = "agesci_theme/forms/select_multiplo_a_discesa.html"
    option_template_name = "agesci_theme/forms/select_multiplo_a_discesa_opzione.html"

    def __init__(self, attrs=None, placeholder=""):
        super().__init__(attrs)
        self.placeholder = placeholder

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["placeholder"] = self.placeholder
        return context

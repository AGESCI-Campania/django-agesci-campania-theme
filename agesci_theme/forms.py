"""Renderer di form Bootstrap 6, opt-in per i progetti consumer.

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

Con lo stesso meccanismo (namespace proprio, nessun renderer richiesto) il
modulo espone i widget dei componenti form nuovi di Bootstrap 6:
``SelettoreData`` (datepicker), ``CodiceOTP``, ``PasswordConRobustezza``,
``InputConAdorno``, ``Combobox``/``ComboboxMultiplo``, ``InputChip`` /
``CampoChip`` e ``Cursore`` (range con bolla e tacche).
"""

import json
import re
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


# ── Widget dei componenti form di Bootstrap 6 ─────────────────────────────
#
# Come SelectMultiploADiscesa, vivono nel namespace agesci_theme/forms/ e
# funzionano anche senza AgesciFormRenderer. Le classi Bootstrap (e
# is-invalid quando il campo ha errori: Django mette aria-invalid negli attrs)
# si calcolano qui, non nel template attrs.html del renderer.
# Il comportamento è del JS di Bootstrap 6 (bundle caricato da base.html):
# non funzionano col tema CoreUI, che è su Bootstrap 5.3.


def _ha_errori(attrs):
    return "aria-invalid" in attrs


def _classi(*classi):
    return " ".join(c for c in classi if c)


class _WidgetBootstrap6:
    """Mixin: aggiunge ``classe_input`` (e ``is-invalid`` se il campo ha
    errori) alla classe dell'``<input>``, ed espone ``widget.invalido``."""

    classe_input = "form-control"
    invalido_sull_input = True

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        attrs = context["widget"]["attrs"]
        invalido = _ha_errori(attrs)
        context["widget"]["invalido"] = invalido
        attrs["class"] = _classi(
            self.classe_input,
            attrs.get("class", ""),
            "is-invalid" if invalido and self.invalido_sull_input else "",
        )
        return context


_FORMATO_DATA_IT = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{4})$")
_FORMATO_DATA_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class SelettoreData(_WidgetBootstrap6, forms.DateInput):
    """``DateInput`` con il datepicker di Bootstrap 6 (calendario a
    comparsa, Vanilla Calendar Pro già incluso nel bundle).

    Il valore viaggia in ISO (``AAAA-MM-GG``): il datepicker lo legge
    all'avvio e lo mostra come ``GG/MM/AAAA``. Al submit il campo contiene
    ``GG/MM/AAAA``: ``value_from_datadict`` lo riconverte in ISO, così il
    ``DateField`` lo accetta qualunque sia ``LANGUAGE_CODE``.

    Uso::

        data = forms.DateField(widget=SelettoreData(data_min="2026-01-01"))

    ``data_min``/``data_max``: stringhe ``AAAA-MM-GG`` o ``date``.
    """

    template_name = "agesci_theme/forms/selettore_data.html"
    # Il datepicker usa type="text": con type="date" si aprirebbe anche il calendario del browser.
    input_type = "text"

    def __init__(self, attrs=None, data_min=None, data_max=None, locale="it-IT"):
        super().__init__(attrs, format="%Y-%m-%d")
        self.data_min = data_min
        self.data_max = data_max
        self.locale = locale

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        attrs = context["widget"]["attrs"]
        attrs.setdefault("autocomplete", "off")
        attrs["data-bs-toggle"] = "datepicker"
        attrs["data-bs-locale"] = self.locale
        attrs["data-bs-date-format"] = '{"day":"2-digit","month":"2-digit","year":"numeric"}'
        if self.data_min:
            attrs["data-bs-date-min"] = str(self.data_min)
        if self.data_max:
            attrs["data-bs-date-max"] = str(self.data_max)
        # Con una data già presente il datepicker va creato al caricamento (non al
        # focus), altrimenti il campo mostra l'ISO finché non lo si tocca.
        valore = context["widget"]["value"]
        if isinstance(valore, str) and _FORMATO_DATA_ISO.match(valore):
            attrs["data-bs-selected-dates"] = json.dumps([valore])
        return context

    def value_from_datadict(self, data, files, name):
        valore = super().value_from_datadict(data, files, name)
        if isinstance(valore, str):
            trovato = _FORMATO_DATA_IT.match(valore.strip())
            if trovato:
                giorno, mese, anno = trovato.groups()
                return f"{anno}-{int(mese):02d}-{int(giorno):02d}"
        return valore


class CodiceOTP(_WidgetBootstrap6, forms.TextInput):
    """Codice di verifica / PIN (OTP input di Bootstrap 6): un solo
    ``<input>`` reso come caselle separate, con incolla e autofill
    (``autocomplete="one-time-code"``).

    lunghezza: numero di caselle (``maxlength``).
    tipo: ``"numeric"`` (default) | ``"alphanumeric"`` | ``"alpha"``.
    gruppi: es. ``[3, 3]`` per un separatore a metà.
    maschera: ``True`` mostra un pallino al posto dei caratteri.
    connesso: ``True`` (default) unisce le caselle in un unico campo.
    """

    template_name = "agesci_theme/forms/codice_otp.html"
    classe_input = "otp-input"
    invalido_sull_input = False

    def __init__(self, attrs=None, lunghezza=6, tipo="numeric", gruppi=None, maschera=False, connesso=True):
        super().__init__(attrs)
        self.lunghezza = lunghezza
        self.tipo = tipo
        self.gruppi = gruppi
        self.maschera = maschera
        self.connesso = connesso

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["attrs"]["maxlength"] = self.lunghezza
        context["widget"].update(
            tipo=self.tipo,
            gruppi=json.dumps(self.gruppi) if self.gruppi else "",
            maschera=self.maschera,
            connesso=self.connesso,
        )
        return context


MESSAGGI_ROBUSTEZZA = {"weak": "Debole", "fair": "Sufficiente", "good": "Buona", "strong": "Robusta"}


class PasswordConRobustezza(_WidgetBootstrap6, forms.PasswordInput):
    """``PasswordInput`` con il pulsante mostra/nascondi del tema e
    l'indicatore di robustezza di Bootstrap 6 (barra a 4 segmenti e testo).

    L'indicatore è solo un aiuto visivo: la validazione resta quella di
    ``AUTH_PASSWORD_VALIDATORS``. ``lunghezza_minima`` (default 8) è la
    soglia del primo segmento; ``messaggi`` sostituisce i testi italiani.
    """

    template_name = "agesci_theme/forms/password_robustezza.html"

    def __init__(self, attrs=None, render_value=False, lunghezza_minima=8, messaggi=None):
        super().__init__(attrs, render_value)
        self.lunghezza_minima = lunghezza_minima
        self.messaggi = {**MESSAGGI_ROBUSTEZZA, **(messaggi or {})}

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["lunghezza_minima"] = self.lunghezza_minima
        context["widget"]["messaggi"] = json.dumps(self.messaggi)
        return context


class InputConAdorno(_WidgetBootstrap6, forms.TextInput):
    """Campo con un testo o un'icona DENTRO il bordo (form adorn di
    Bootstrap 6), es. ``€`` per gli importi o ``@agesci.it`` per le email.

    prefisso / suffisso: testo prima o dopo il valore (uno dei due).
    icona: markup SVG (es. ``bs_icon("search")``), al posto del testo.
    input_type: ``"text"`` (default), ``"email"``, ``"search"``, ``"number"``…
    """

    template_name = "agesci_theme/forms/input_con_adorno.html"
    classe_input = "form-ghost"
    invalido_sull_input = False

    def __init__(self, attrs=None, prefisso="", suffisso="", icona="", input_type=None):
        super().__init__(attrs)
        if prefisso and suffisso:
            raise ValueError("InputConAdorno: usa prefisso oppure suffisso, non entrambi.")
        self.prefisso = prefisso
        self.suffisso = suffisso
        self.icona = icona
        if input_type:
            self.input_type = input_type

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"].update(
            adorno=self.prefisso or self.suffisso,
            icona=self.icona,
            alla_fine=bool(self.suffisso),
        )
        return context


class _ComboboxMixin:
    """Combobox di Bootstrap 6: bottone + menu, il JS crea un
    ``<input type="hidden" name=...>`` col valore (più valori separati da
    virgola, per la variante multipla)."""

    template_name = "agesci_theme/forms/combobox.html"
    option_template_name = "agesci_theme/forms/combobox_opzione.html"
    multiplo = False

    def __init__(self, attrs=None, choices=(), placeholder="", ricerca=False):
        super().__init__(attrs, choices)
        self.placeholder = placeholder
        self.ricerca = ricerca

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        widget = context["widget"]
        widget["placeholder"] = self.placeholder
        widget["ricerca"] = self.ricerca
        widget["multiplo"] = self.multiplo
        widget["invalido"] = _ha_errori(widget["attrs"])
        return context


class Combobox(_ComboboxMixin, forms.Select):
    """``Select`` reso come combobox di Bootstrap 6 (con ``ricerca=True``
    un campo di ricerca filtra le voci).

    Uso::

        provincia = forms.ChoiceField(choices=..., widget=Combobox(ricerca=True))
    """


class ComboboxMultiplo(_ComboboxMixin, forms.SelectMultiple):
    """``SelectMultiple`` reso come combobox multipla di Bootstrap 6: il menu
    resta aperto e il bottone mostra il numero di voci scelte."""

    multiplo = True

    def value_from_datadict(self, data, files, name):
        valori = super().value_from_datadict(data, files, name)
        if not valori:
            return valori
        if isinstance(valori, str):  # dati in un dict semplice, non in una QueryDict
            valori = [valori]
        # Il JS invia un solo campo hidden con i valori separati da virgola.
        if len(valori) == 1 and "," in valori[0]:
            valori = valori[0].split(",")
        return [v for v in valori if v]


class InputChip(forms.Widget):
    """Campo che trasforma ogni voce in un chip (chip input di Bootstrap 6):
    Invio o la virgola creano il chip, Backspace o la "x" lo rimuovono.

    Bootstrap 6 non crea un campo da inviare col form: lo mantiene
    ``agesci_theme/js/chip-input.js`` (``<input type="hidden">`` con i
    valori uniti da virgola). ``value_from_datadict`` restituisce una lista
    di stringhe senza vuoti. Stessa API dell'``InputChip`` di CoreUI.
    """

    template_name = "agesci_theme/forms/input_chip.html"

    def __init__(self, attrs=None, placeholder="", max_chip=None):
        super().__init__(attrs)
        self.placeholder = placeholder
        self.max_chip = max_chip

    def format_value(self, value):
        if not value:
            return []
        if isinstance(value, str):
            value = value.split(",")
        return [str(v).strip() for v in value if str(v).strip()]

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        widget = context["widget"]
        widget["placeholder"] = self.placeholder
        widget["max_chip"] = self.max_chip
        widget["invalido"] = _ha_errori(widget["attrs"])
        widget["valore_unito"] = ",".join(widget["value"])
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
    limita il numero di voci (anche nel browser).
    """

    widget = InputChip
    default_error_messages = {
        "max_chip": "Inserisci al massimo %(max)d voci.",
    }

    def __init__(self, *, max_chip=None, **kwargs):
        self.max_chip = max_chip
        super().__init__(**kwargs)
        if max_chip is not None and isinstance(self.widget, InputChip):
            self.widget.max_chip = max_chip

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


class Cursore(_WidgetBootstrap6, forms.NumberInput):
    """Slider (range di Bootstrap 6) con traccia riempita e, opzionali, la
    bolla col valore e le tacche.

    bolla: ``True`` (default) mostra il valore sopra il cursore.
    tacche: lista di ``(valore, etichetta)``; etichetta vuota = solo tacca.
    ``min``/``max``/``step`` vengono dal campo (``IntegerField(min_value=…)``)
    o da ``attrs``.
    """

    template_name = "agesci_theme/forms/cursore.html"
    input_type = "range"
    classe_input = "form-range-input"

    def __init__(self, attrs=None, bolla=True, tacche=None):
        super().__init__(attrs)
        self.bolla = bolla
        self.tacche = tacche or []

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        widget = context["widget"]
        widget["bolla"] = self.bolla
        widget["tacche"] = [{"valore": v, "etichetta": e} for v, e in self.tacche]
        if self.tacche:
            widget["attrs"]["list"] = f"{widget['attrs'].get('id') or name}_tacche"
        return context

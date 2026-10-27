from django import forms
from django.apps import apps
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe
from agesci_theme.forms import SelectMultiploADiscesa
from agesci_theme.templatetags.agesci_tags import ZONE


def components(request):
    context = {
        "breadcrumb_items": [
            {"label": "Home", "url": reverse("home")},
            {"label": "Componenti"},
        ],
        "breadcrumb_demo": [
            {"label": "Home", "url": reverse("home")},
            {"label": "Componenti"},
        ],
        "breadcrumb_demo_long": [
            {"label": "Home", "url": reverse("home")},
            {"label": "Sezione", "url": "#"},
            {"label": "Sotto-sezione", "url": "#"},
            {"label": "Pagina corrente"},
        ],
        "demo_features": [
            {"icon": "people-fill",  "title": "Comunità",   "description": "Un movimento di oltre 180.000 soci."},
            {"icon": "geo-alt-fill", "title": "Territorio", "description": "Presente in ogni zona della Campania."},
            {"icon": "star-fill",    "title": "Formazione", "description": "Percorsi educativi per tutte le età."},
            {"icon": "heart-fill",   "title": "Valori",     "description": "Lealtà, servizio, fraternità."},
        ],
        "demo_dropdown": [
            {"label": "Profilo",      "url": "#"},
            {"label": "Impostazioni", "url": "#"},
            {"divider": True},
            {"label": "Esci",         "url": "#"},
        ],
        "demo_list_group": [
            {"label": "Branca L/C", "badge": "12"},
            {"label": "Branca E/G", "badge": "8"},
            {"label": "Branca R/S", "badge": "5", "active": True},
            {"label": "Capi",       "badge": "3"},
        ],
        "demo_masonry": [
            {"content": mark_safe("<p>Card 1: breve testo di esempio.</p>")},
            {"content": mark_safe("<p>Card 2: testo più lungo per mostrare l'effetto masonry con altezze diverse.</p><p>Secondo paragrafo.</p>")},
            {"content": mark_safe("<p>Card 3.</p>")},
            {"content": mark_safe("<p>Card 4: altro testo di lunghezza media per la griglia.</p>")},
            {"content": mark_safe("<p>Card 5.</p>")},
            {"content": mark_safe("<p>Card 6: testo conclusivo.</p>")},
        ],
    }
    return render(request, "components.html", context)


class DemoForm(forms.Form):
    """Form di esempio per la demo di AgesciFormRenderer (docs/forms.md):
    esercita form-control/is-invalid, il toggle mostra/nascondi password e
    invalid-feedback, senza passare da allauth."""

    nome = forms.CharField(label="Nome", max_length=100)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    interessi = forms.MultipleChoiceField(
        label="Interessi",
        choices=[
            ("scautismo", "Scautismo"),
            ("formazione", "Formazione"),
            ("territorio", "Territorio"),
            ("internazionale", "Internazionale"),
        ],
        required=False,
        widget=SelectMultiploADiscesa(placeholder="Nessuno"),
    )


def _demo_form_class():
    """Con il tema CoreUI (config.settings_coreui) il form aggiunge un campo
    CampoChip, che richiede il JS di CoreUI caricato da agesci_coreui/base.html."""
    if not apps.is_installed("agesci_coreui"):
        return DemoForm
    from agesci_coreui.forms import CampoChip, InputChip

    class DemoFormCoreUI(DemoForm):
        tag = CampoChip(
            label="Tag",
            required=False,
            max_chip=5,
            widget=InputChip(placeholder="Scrivi e premi Invio…"),
            help_text="Campo CampoChip / InputChip (chip-input di CoreUI), max 5 voci.",
        )

    return DemoFormCoreUI


def form_demo(request):
    form_class = _demo_form_class()
    if request.method == "POST":
        form = form_class(request.POST)
        form.is_valid()
    elif request.GET.get("invalid"):
        form = form_class({})
        form.is_valid()
    else:
        form = form_class()
    return render(request, "form_demo.html", {"form": form})


def form_demo_errori(request):
    """Il form di form_demo validato a vuoto, per mostrare gli errori."""
    form = _demo_form_class()({})
    form.is_valid()
    return render(request, "form_demo.html", {"form": form})


_BRANCHE = [
    ("generico", "Generico"),
    ("capi", "Capi"),
    ("lc", "L/C"),
    ("eg", "E/G"),
    ("rs", "R/S"),
    ("viola", "Viola"),
    ("generico2", "Generico 2"),
]


def home(request):
    context = {
        "branche": _BRANCHE,
        "breadcrumb_items": [
            {"label": "Demo AGESCI Campania", "url": reverse("home")},
            {"label": "Home"},
        ],
        "zone_list": sorted(ZONE.keys()),
        "demo_breadcrumb": [
            {"label": "Home", "url": reverse("home")},
            {"label": "Demo v2"},
        ],
        "demo_features": [
            {"icon": "people-fill",  "title": "Comunità",    "description": "Un movimento di oltre 180.000 soci in tutta Italia."},
            {"icon": "geo-alt-fill", "title": "Territorio",  "description": "Presente in ogni zona della Regione Campania."},
            {"icon": "star-fill",    "title": "Formazione",  "description": "Percorsi educativi per tutte le fasce d'età."},
        ],
        "demo_dropdown": [
            {"label": "Profilo",   "url": "#"},
            {"label": "Impostazioni", "url": "#"},
            {"divider": True},
            {"label": "Esci",      "url": "#"},
        ],
        "demo_list_group": [
            {"label": "Branca L/C",  "badge": "12"},
            {"label": "Branca E/G",  "badge": "8"},
            {"label": "Branca R/S",  "badge": "5", "active": True},
            {"label": "Capi",        "badge": "3"},
        ],
    }
    return render(request, "home.html", context)

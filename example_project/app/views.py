from django import forms
from django.shortcuts import render
from django.utils.safestring import mark_safe
from agesci_theme.forms import SelectMultiploADiscesa
from agesci_theme.templatetags.agesci_tags import ZONE


def components(request):
    context = {
        "breadcrumb_items": [
            {"label": "Home", "url": "/"},
            {"label": "Componenti"},
        ],
        "breadcrumb_demo": [
            {"label": "Home", "url": "/"},
            {"label": "Componenti"},
        ],
        "breadcrumb_demo_long": [
            {"label": "Home", "url": "/"},
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


def form_demo(request):
    if request.method == "POST":
        form = DemoForm(request.POST)
        form.is_valid()
    elif request.GET.get("invalid"):
        form = DemoForm({})
        form.is_valid()
    else:
        form = DemoForm()
    return render(request, "form_demo.html", {"form": form})


_BRANCHE = [
    ("generico", "Generico"),
    ("capi", "Capi"),
    ("lc", "L/C"),
    ("eg", "E/G"),
    ("rs", "R/S"),
    ("viola", "Viola"),
]


def home(request):
    context = {
        "branche": _BRANCHE,
        "breadcrumb_items": [
            {"label": "Demo AGESCI Campania", "url": "/"},
            {"label": "Home"},
        ],
        "zone_list": sorted(ZONE.keys()),
        "demo_breadcrumb": [
            {"label": "Home", "url": "/"},
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

from django import forms
from django.apps import apps
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.utils.safestring import mark_safe
from agesci_theme.forms import (
    CampoChip,
    CodiceOTP,
    Combobox,
    ComboboxMultiplo,
    Cursore,
    InputChip,
    InputConAdorno,
    PasswordConRobustezza,
    SelectMultiploADiscesa,
    SelettoreData,
)
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
        # Componenti nuovi di Bootstrap 6 (_components_bs6.html, solo tema Bootstrap 6)
        "demo_accordion": [
            {"title": "Cos'è il reparto?", "content": mark_safe("<p>L'unità della branca <strong>E/G</strong>, dagli 11 ai 16 anni.</p>"), "open": True},
            {"title": "Quando ci si incontra?", "content": "Ogni settimana, più uscite e campi durante l'anno."},
            {"title": "Come ci si iscrive?", "content": "Contattando il gruppo scout più vicino."},
        ],
        "demo_passi": ["Dati personali", "Gruppo", "Quota", "Conferma"],
        "demo_passi_link": [
            {"label": "Iscrizione", "url": "#"},
            {"label": "Pagamento", "url": "#"},
            {"label": "Fatto", "url": "#"},
        ],
        "demo_carousel": [
            {"image_url": static("app/demo/slide-1.svg"), "alt": "Montagne verdi", "title": "Route estiva", "text": "Due settimane di cammino in Appennino."},
            {"image_url": static("app/demo/slide-2.svg"), "alt": "Montagne blu", "title": "Campo al lago"},
            {"image_url": static("app/demo/slide-3.svg"), "alt": "Montagne viola"},
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


_ZONE_DEMO = [
    ("Napoli", [("napoli-centro", "Napoli Centro"), ("flegrea", "Flegrea"), ("vesuviana", "Vesuviana")]),
    ("Salerno", [("salerno", "Salerno"), ("cilento", "Cilento"), ("agro", "Agro Nocerino")]),
    ("Altre", [("caserta", "Caserta"), ("benevento", "Benevento"), ("irpinia", "Irpinia")]),
]


class DemoFormBootstrap6(DemoForm):
    """I widget dei componenti form nuovi di Bootstrap 6 (agesci_theme.forms).
    Solo col tema Bootstrap 6: il loro markup e il loro JS non esistono in CoreUI 5."""

    nuova_password = forms.CharField(
        label="Nuova password",
        required=False,
        widget=PasswordConRobustezza(attrs={"autocomplete": "new-password"}),
        help_text="PasswordConRobustezza: toggle + indicatore di robustezza.",
    )
    data_evento = forms.DateField(
        label="Data dell'evento",
        widget=SelettoreData(data_min="2026-01-01", data_max="2027-12-31"),
        help_text="SelettoreData (datepicker), solo date 2026–2027.",
    )
    codice = forms.CharField(
        label="Codice di verifica",
        min_length=6,
        max_length=6,
        widget=CodiceOTP(gruppi=[3, 3]),
        help_text="CodiceOTP: 6 cifre, incolla anche un codice tipo 123-456.",
    )
    quota = forms.DecimalField(
        label="Quota",
        required=False,
        decimal_places=2,
        localize=True,
        widget=InputConAdorno(prefisso="€", attrs={"inputmode": "decimal", "placeholder": "0,00"}),
        help_text="InputConAdorno con prefisso.",
    )
    utente = forms.CharField(
        label="Utente",
        required=False,
        widget=InputConAdorno(suffisso="@agesci.it"),
        help_text="InputConAdorno con suffisso.",
    )
    zona = forms.ChoiceField(
        label="Zona",
        choices=_ZONE_DEMO,
        widget=Combobox(placeholder="Scegli una zona…", ricerca=True),
        help_text="Combobox con ricerca e gruppi.",
    )
    branche = forms.MultipleChoiceField(
        label="Branche",
        required=False,
        choices=[("lc", "L/C"), ("eg", "E/G"), ("rs", "R/S"), ("capi", "Capi")],
        widget=ComboboxMultiplo(placeholder="Nessuna"),
        help_text="ComboboxMultiplo.",
    )
    tag = CampoChip(
        label="Tag",
        required=False,
        max_chip=5,
        widget=InputChip(placeholder="Scrivi e premi Invio…"),
        help_text="CampoChip / InputChip (chip input di Bootstrap 6), max 5 voci.",
    )
    partecipanti = forms.IntegerField(
        label="Partecipanti",
        min_value=0,
        max_value=100,
        step_size=5,
        initial=30,
        widget=Cursore(tacche=[(0, "0"), (25, ""), (50, "50"), (75, ""), (100, "100")]),
        help_text="Cursore (range) con bolla e tacche.",
    )


def _demo_form_class():
    """Col tema Bootstrap 6 il form aggiunge i widget dei componenti nuovi di
    Bootstrap 6; con CoreUI (config.settings_coreui) un campo CampoChip, che
    richiede il JS di CoreUI caricato da agesci_coreui/base.html."""
    if not apps.is_installed("agesci_coreui"):
        return DemoFormBootstrap6
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

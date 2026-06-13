from django.shortcuts import render
from agesci_theme.templatetags.agesci_tags import ZONE


def home(request):
    context = {
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

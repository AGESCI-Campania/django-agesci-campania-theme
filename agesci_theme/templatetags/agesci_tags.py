"""Template tag di utilita' del tema AGESCI.

Uso nei template:
    {% load agesci_tags %}
    {% emblema_zona "napoli" css_class="img-fluid" %}
    <span class="badge {% branca_bg %}">...</span>
"""
from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()

# Zone della Regione Campania -> file PNG negli static
ZONE = {
    "caserta": "CAMPANIA_CASERTA.png",
    "faito": "CAMPANIA_FAITO.png",
    "felix": "CAMPANIA_FELIX.png",
    "hirpinia": "CAMPANIA_HIRPINIA.png",
    "liternum": "CAMPANIA_LITERNUM.png",
    "napoli": "CAMPANIA_NAPOLI.png",
    "poseidonia": "CAMPANIA_POSEIDONIA.png",
    "salerno": "CAMPANIA_SALERNO.png",
    "samnium": "CAMPANIA_SAMNIUM.png",
    "vesuvio": "CAMPANIA_VESUVIO.png",
    "volturno": "CAMPANIA_VOLTURNO.png",
}

# Branca -> classe utility di background del tema
_BRANCA_BG = {
    "capi": "bg-ag-viola",
    "viola": "bg-ag-viola",
    "generico": "bg-ag-azzurro",
    "lc": "bg-ag-giallo-lc",
    "eg": "bg-ag-verde-eg",
    "rs": "bg-ag-rosso-rs",
}


@register.simple_tag
def emblema_zona(zona, css_class="", alt=""):
    """Restituisce un tag <img> dell'emblema di una Zona Campania."""
    key = (zona or "").strip().lower()
    if key not in ZONE:
        return ""
    src = static(f"agesci_theme/img/zone/{ZONE[key]}")
    alt = alt or f"Zona {key.capitalize()}"
    return mark_safe(f'<img src="{src}" class="{css_class}" alt="{alt}">')


@register.simple_tag
def zone_disponibili():
    """Lista ordinata delle chiavi di zona disponibili."""
    return sorted(ZONE.keys())


@register.simple_tag(takes_context=True)
def branca_bg(context):
    """Classe CSS di background corrispondente alla branca corrente."""
    branca = context.get("agesci_theme_branca", "generico")
    return _BRANCA_BG.get(branca, "bg-ag-azzurro")

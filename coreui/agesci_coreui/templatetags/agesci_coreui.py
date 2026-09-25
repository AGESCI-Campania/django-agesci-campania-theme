"""Componenti free di CoreUI 5 per il tema AGESCI (layout CoreUI).

Richiedono ``agesci_coreui/base.html`` (che carica coreui.min.css e
coreui.bundle.min.js). I componenti Bootstrap del tema base
(``{% load agesci_components %}``) restano utilizzabili così come sono.

Uso nei template:
    {% load agesci_coreui %}
    {% ag_nav_title "Gestione" %}
    {% ag_nav_item "Home" "/" icon="house-fill" active=True %}
    {% ag_callout title="Attenzione" text="..." variant="warning" %}
    {% ag_avatar name="Mario Rossi" status="success" %}
    {% ag_chip "E/G" variant="success" %}
"""
from django import template
from django.apps import apps

register = template.Library()


def _icona(nome, classi):
    """SVG di Bootstrap Icons via django-bootstrap-icons (extra opzionale
    ``[icons]`` del tema base). Senza l'app installata l'icona è omessa."""
    if not nome or not apps.is_installed("django_bootstrap_icons"):
        return ""
    from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon

    return bs_icon(nome, extra_classes=classi)


@register.inclusion_tag("agesci_coreui/components/nav_title.html")
def ag_nav_title(label):
    """Titolo di sezione nella ``.sidebar-nav`` (blocco ``sidebar_items``)."""
    return {"label": label}


@register.inclusion_tag("agesci_coreui/components/nav_item.html", takes_context=True)
def ag_nav_item(context, label, url="#", icon="", active=None, badge="", badge_variant="primary"):
    """Voce della ``.sidebar-nav`` (blocco ``sidebar_items``).

    icon: nome Bootstrap Icon (es. "house-fill"); richiede l'extra ``[icons]``
    active: True/False per forzare l'evidenziazione; se omesso la voce è
        attiva quando ``url`` coincide con ``request.path``
    badge: testo di un badge opzionale allineato a destra
    """
    if active is None:
        request = context.get("request")
        active = request is not None and url == request.path
    return {
        "label": label,
        "url": url,
        "icon": _icona(icon, "nav-icon"),
        "active": active,
        "badge": badge,
        "badge_variant": badge_variant,
    }


@register.inclusion_tag("agesci_coreui/components/callout.html")
def ag_callout(title="", text="", variant="primary"):
    """Callout CoreUI (riquadro con bordo sinistro colorato).

    variant: "primary" (colore della branca) | "secondary" | "success" |
    "danger" | "warning" | "info" | "light" | "dark"
    """
    return {"title": title, "text": text, "variant": variant}


def _iniziali(nome):
    parole = [p for p in (nome or "").split() if p]
    return "".join(p[0] for p in parole[:2]).upper()


@register.inclusion_tag("agesci_coreui/components/avatar.html")
def ag_avatar(name="", image_url="", size="md", status=""):
    """Avatar CoreUI: immagine se ``image_url``, altrimenti le iniziali di
    ``name`` sul colore della branca.

    size: "sm" | "md" (default) | "lg" | "xl"
    status: "" | "success" | "warning" | "danger" | "secondary" (pallino di stato)
    """
    return {
        "name": name,
        "iniziali": _iniziali(name),
        "image_url": image_url,
        "size": size,
        "status": status,
    }


@register.inclusion_tag("agesci_coreui/components/chip.html")
def ag_chip(label, variant="", icon=""):
    """Chip CoreUI statico (etichetta compatta).

    variant: "" (neutro) | "primary" (colore della branca) | "success" | …
    icon: nome Bootstrap Icon opzionale; richiede l'extra ``[icons]``
    Per un campo di form con chip modificabili usa il widget
    ``agesci_coreui.forms.InputChip``.
    """
    return {"label": label, "variant": variant, "icon": _icona(icon, "chip-icon")}

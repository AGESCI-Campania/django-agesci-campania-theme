"""Componenti opzionali del tema AGESCI v2.

Uso nei template:
    {% load agesci_components %}
    {% ag_hero title="Benvenuto" subtitle="Testo di esempio" %}
    {% ag_feature_card icon="star-fill" title="Funzionalità" description="..." %}
"""
from django import template

register = template.Library()


@register.inclusion_tag("agesci_theme/components/hero.html")
def ag_hero(title="", subtitle="", cta_text="", cta_url="#", variant="subtle", image_url=""):
    """Hero section.

    variant: "subtle" (default) | "primary" | "dark" | "centered"
    """
    return {
        "title": title,
        "subtitle": subtitle,
        "cta_text": cta_text,
        "cta_url": cta_url,
        "variant": variant,
        "image_url": image_url,
    }


@register.inclusion_tag("agesci_theme/components/feature_card.html")
def ag_feature_card(title="", description="", icon="", variant=""):
    """Card singola della sezione features con icona Bootstrap Icon.

    icon: nome dell'icona Bootstrap (es. "star-fill", "people-fill")
    variant: classe Bootstrap per il colore icona (es. "text-primary") — default: colore tema
    """
    return {"title": title, "description": description, "icon": icon, "variant": variant}


@register.inclusion_tag("agesci_theme/components/feature_grid.html")
def ag_feature_grid(items, cols=3):
    """Griglia di feature card.

    items: lista di dict con chiavi title, description, icon, variant (opzionale)
    cols: numero di colonne su desktop (2, 3 o 4)
    """
    col_class = {2: "col-md-6", 3: "col-md-4", 4: "col-md-3"}.get(cols, "col-md-4")
    return {"items": items, "col_class": col_class}


@register.inclusion_tag("agesci_theme/components/jumbotron.html")
def ag_jumbotron(title="", lead="", cta_text="", cta_url="#", variant=""):
    """Jumbotron (rimosso da BS5, riproposto come componente custom).

    variant: "" (default, sfondo primary-subtle) | "primary"
    """
    return {
        "title": title,
        "lead": lead,
        "cta_text": cta_text,
        "cta_url": cta_url,
        "variant": variant,
    }


@register.inclusion_tag("agesci_theme/components/badge.html")
def ag_badge(text="", variant="primary", pill=False):
    """Badge Bootstrap con colori del tema.

    variant: "primary" | "secondary" | "success" | "danger" | "warning" | "info" | "light" | "dark"
    pill: True per border-radius massimo
    """
    return {"text": text, "variant": variant, "pill": pill}


@register.inclusion_tag("agesci_theme/components/button.html")
def ag_button(label="", variant="primary", size="", outline=False, href="", type="button"):
    """Bottone Bootstrap.

    outline: True per variante outline
    href: se valorizzato, renderizza un <a> invece di <button>
    size: "sm" | "lg" | ""
    """
    return {
        "label": label,
        "variant": variant,
        "size": size,
        "outline": outline,
        "href": href,
        "type": type,
    }


@register.inclusion_tag("agesci_theme/components/breadcrumb.html")
def ag_breadcrumb(items=None):
    """Breadcrumb con stile del tema.

    items: lista di dict con chiavi label e url (url opzionale per l'ultimo elemento)
    Esempio: [{"label": "Home", "url": "/"}, {"label": "Pagina corrente"}]
    """
    return {"items": items or []}


@register.inclusion_tag("agesci_theme/components/dropdown.html")
def ag_dropdown(label="", items=None, variant="primary", split=False, direction=""):
    """Dropdown Bootstrap.

    items: lista di dict con chiavi label e url; usa {"divider": True} per separatore
    split: True per bottone split
    direction: "" | "dropup" | "dropstart" | "dropend"
    """
    return {
        "label": label,
        "items": items or [],
        "variant": variant,
        "split": split,
        "direction": direction,
    }


@register.inclusion_tag("agesci_theme/components/list_group.html")
def ag_list_group(items=None, flush=False, numbered=False):
    """List group Bootstrap.

    items: lista di dict con chiavi label, url (opz.), active (opz.), badge (opz.)
    flush: True per rimuovere i bordi laterali
    numbered: True per lista numerata
    """
    return {"items": items or [], "flush": flush, "numbered": numbered}


@register.inclusion_tag("agesci_theme/components/modal_trigger.html")
def ag_modal_trigger(modal_id, label="Apri", variant="primary", size=""):
    """Bottone che apre un modal Bootstrap.

    Accoppiato con il template agesci_theme/components/modal.html (via {% include %}).
    size: "sm" | "lg" | ""
    """
    return {"modal_id": modal_id, "label": label, "variant": variant, "size": size}


@register.inclusion_tag("agesci_theme/components/masonry_grid.html")
def ag_masonry_grid(items=None, cols=3):
    """Griglia Masonry (richiede masonry-layout JS nel blocco extra_js).

    items: lista di dict con chiave content (HTML come mark_safe)
    cols: numero di colonne (2, 3 o 4)

    Caricamento Masonry nel template:
        {% block extra_js %}{{ block.super }}
        <script src="https://cdn.jsdelivr.net/npm/masonry-layout@4/dist/masonry.pkgd.min.js" defer></script>
        {% endblock %}
    """
    col_class = {2: "col-md-6", 3: "col-md-4", 4: "col-md-3"}.get(cols, "col-md-4")
    return {"items": items or [], "col_class": col_class}

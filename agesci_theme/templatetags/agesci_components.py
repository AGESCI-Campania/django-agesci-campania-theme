"""Componenti opzionali del tema AGESCI.

Uso nei template:
    {% load agesci_components %}
    {% ag_hero title="Benvenuto" subtitle="Testo di esempio" %}
    {% ag_feature_card icon="star-fill" title="Funzionalità" description="..." %}
"""
import json
import uuid

from django import template
from django.apps import apps

from agesci_theme.forms import MESSAGGI_ROBUSTEZZA

register = template.Library()

# Bootstrap 6 non ha theme-light / theme-dark: dark -> inverse, light -> secondary.
_THEME_BS6 = {"dark": "inverse", "light": "secondary"}


def _theme(variant):
    """Nome del tema Bootstrap 6 (classe ``theme-<nome>``) per una variante v5."""
    return _THEME_BS6.get(variant, variant)


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
    variant: classe Bootstrap per il colore icona (es. "fg-primary") — default: colore tema
    """
    return {"title": title, "description": description, "icon": icon, "variant": variant}


@register.inclusion_tag("agesci_theme/components/feature_grid.html")
def ag_feature_grid(items, cols=3):
    """Griglia di feature card.

    items: lista di dict con chiavi title, description, icon, variant (opzionale)
    cols: numero di colonne su desktop (2, 3 o 4)
    """
    row_cols_class = {2: "md:row-cols-2", 3: "md:row-cols-3", 4: "md:row-cols-4"}.get(cols, "md:row-cols-3")
    return {"items": items, "cols": cols, "row_cols_class": row_cols_class}


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
    (in Bootstrap 6: theme-<variant>; "dark" -> theme-inverse, "light" -> theme-secondary)
    pill: True per border-radius massimo
    """
    return {"text": text, "variant": variant, "theme": _theme(variant), "pill": pill}


@register.inclusion_tag("agesci_theme/components/button.html")
def ag_button(label="", variant="primary", size="", outline=False, href="", type="button"):
    """Bottone Bootstrap.

    variant: "primary" | "secondary" | "success" | "danger" | "warning" | "info" | "light" | "dark"
    (theme-<variant> in Bootstrap 6, "dark" -> inverse, "light" -> secondary) oppure "link"
    (bottone testuale ``btn btn-link``)
    outline: True per variante outline
    href: se valorizzato, renderizza un <a> invece di <button>
    size: "sm" | "lg" | ""
    """
    return {
        "label": label,
        "variant": variant,
        "theme": _theme(variant),
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
    """Menu Bootstrap 6 (ex dropdown).

    items: lista di dict con chiavi label e url; usa {"divider": True} per separatore
    split: True per bottone split
    direction: "" | "dropup" | "dropstart" | "dropend" (-> data-bs-placement)
    """
    return {
        "label": label,
        "items": items or [],
        "variant": variant,
        "theme": _theme(variant),
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
    """Bottone che apre un dialog Bootstrap 6 (ex modal).

    Accoppiato con il template agesci_theme/components/modal.html (via {% include %}).
    size: "sm" | "lg" | ""
    """
    return {"modal_id": modal_id, "label": label, "variant": variant, "theme": _theme(variant), "size": size}


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
    col_class = {2: "md:col-6", 3: "md:col-4", 4: "md:col-3"}.get(cols, "md:col-4")
    return {"items": items or [], "cols": cols, "col_class": col_class}


@register.inclusion_tag("agesci_theme/components/password_field.html")
def ag_password_field(
    name="password",
    id="",
    label="",
    value="",
    placeholder="",
    help_text="",
    errors=None,
    required=False,
    autocomplete="current-password",
    strength=False,
    min_length=8,
):
    """Campo password con pulsante mostra/nascondi (icona SVG inline).

    strength=True aggiunge l'indicatore di robustezza di Bootstrap 6
    (come il widget ``PasswordConRobustezza``; ``min_length`` è la soglia
    del primo segmento). Ha senso con ``autocomplete="new-password"``.

    Utilizzabile in qualsiasi form, anche senza attivare FORM_RENDERER —
    non dipende dal meccanismo AgesciFormRenderer (vedi agesci_theme.forms):

        {% ag_password_field name="password" label="Password" required=True %}

    Con un form Django, passa i valori dal campo esplicitamente:

        {% ag_password_field name=form.password.html_name id=form.password.id_for_label
           label=form.password.label value=form.password.value
           errors=form.password.errors required=form.password.field.required %}

    Condivide il markup del pulsante toggle con l'override
    django/forms/widgets/password.html usato da AgesciFormRenderer (vedi
    components/_password_toggle_button.html): un'unica fonte per icona e
    comportamento, così un campo disegnato con questo tag e uno
    renderizzato via FORM_RENDERER sono visivamente identici.
    """
    return {
        "name": name,
        "id": id or f"id_{name}",
        "label": label,
        "value": value,
        "placeholder": placeholder,
        "help_text": help_text,
        "errors": errors or [],
        "required": required,
        "autocomplete": autocomplete,
        "strength": strength,
        "min_length": min_length,
        "messaggi": json.dumps(MESSAGGI_ROBUSTEZZA),
    }


@register.inclusion_tag("agesci_theme/components/multiselect_dropdown.html")
def ag_multiselect_dropdown(
    name,
    id="",
    label="",
    choices=None,
    selected=None,
    placeholder="",
    help_text="",
    errors=None,
    required=False,
):
    """Tendina Bootstrap chiusa con checkbox multiple (bottone + dropdown).

    Utilizzabile in qualsiasi form, anche senza attivare FORM_RENDERER —
    non dipende dal meccanismo AgesciFormRenderer (vedi agesci_theme.forms):

        {% ag_multiselect_dropdown name="gruppo" label="Gruppo"
           choices=lista_gruppi placeholder="Tutti" %}

    choices: lista di tuple (value, label), come le choices di Django.
    selected: lista di value già selezionati.

    Condivide il markup del bottone/menu con l'override
    agesci_theme/forms/select_multiplo_a_discesa.html usato dal widget
    SelectMultiploADiscesa (vedi
    components/_multiselect_dropdown_menu.html): un'unica fonte di markup,
    così un campo disegnato con questo tag e uno renderizzato via
    SelectMultiploADiscesa sono visivamente identici.
    """
    selected = set(selected or [])
    options = [
        {"value": value, "label": choice_label, "checked": str(value) in {str(s) for s in selected}}
        for value, choice_label in (choices or [])
    ]
    return {
        "name": name,
        "id": id or f"id_{name}",
        "label": label,
        "options": options,
        "placeholder": placeholder,
        "help_text": help_text,
        "errors": errors or [],
        "required": required,
    }


# ── Componenti nuovi di Bootstrap 6 ───────────────────────────────────────


def _id_univoco(prefisso):
    return f"{prefisso}-{uuid.uuid4().hex[:8]}"


def _icona(nome, classi=""):
    """SVG di Bootstrap Icons via django-bootstrap-icons (extra opzionale
    ``[icons]``). Senza l'app installata l'icona è omessa."""
    if not nome or not apps.is_installed("django_bootstrap_icons"):
        return ""
    from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon

    return bs_icon(nome, extra_classes=classi)


@register.inclusion_tag("agesci_theme/components/accordion.html")
def ag_accordion(items=None, id="", always_open=False, flush=False, gap=False, size="", variant=""):
    """Accordion Bootstrap 6 (``<details>`` nativi, nessun JS).

    items: lista di dict con chiavi title, content (HTML con mark_safe) e
    open (opzionale, voce aperta al caricamento).
    always_open: True per lasciare aperte più voci insieme (di default
    aprirne una chiude le altre).
    flush: senza bordi esterni; gap: voci separate; size: "" | "sm".
    variant: colore della voce aperta, es. "primary" (colore della branca).
    """
    return {
        "items": items or [],
        "name": id or _id_univoco("ag-accordion"),
        "always_open": always_open,
        "flush": flush,
        "gap": gap,
        "size": size,
        "theme": _theme(variant),
    }


def _iniziali(nome):
    parole = [p for p in (nome or "").split() if p]
    return "".join(p[0] for p in parole[:2]).upper()


# Stato dell'avatar: nomi CoreUI (success/warning/…) -> classi Bootstrap 6.
_STATO_AVATAR = {
    "success": "online", "online": "online",
    "secondary": "offline", "offline": "offline",
    "danger": "busy", "busy": "busy",
    "warning": "away", "away": "away",
}
_STATO_AVATAR_COREUI = {"online": "success", "offline": "secondary", "busy": "danger", "away": "warning"}
_STATO_AVATAR_ETICHETTA = {"online": "In linea", "offline": "Non in linea", "busy": "Occupato", "away": "Assente"}


@register.inclusion_tag("agesci_theme/components/avatar.html")
def ag_avatar(name="", image_url="", size="md", status="", variant="primary", subtle=False):
    """Avatar Bootstrap 6: immagine se ``image_url``, altrimenti le iniziali
    di ``name`` (di default sul colore della branca).

    size: "xs" | "sm" | "md" (default) | "lg" | "xl"
    status: "" | "online" | "away" | "busy" | "offline" (accetta anche i
    nomi CoreUI "success" | "warning" | "danger" | "secondary")
    variant / subtle: colore delle iniziali (theme-<variant>, avatar-subtle)

    Stessa firma di ``ag_avatar`` del tema CoreUI, che ha una copia propria
    di questo template.
    """
    stato = _STATO_AVATAR.get(status, "")
    return {
        "name": name,
        "iniziali": _iniziali(name),
        "image_url": image_url,
        "size": size,
        "stato": stato,
        "stato_etichetta": _STATO_AVATAR_ETICHETTA.get(stato, ""),
        "status": _STATO_AVATAR_COREUI.get(stato, ""),
        "theme": _theme(variant),
        "subtle": subtle,
    }


@register.inclusion_tag("agesci_theme/components/chip.html")
def ag_chip(label, variant="", icon="", active=False):
    """Chip Bootstrap 6 statico (etichetta compatta e tenue).

    variant: "" (neutro) | "primary" (colore della branca) | "success" | …
    icon: nome Bootstrap Icon opzionale; richiede l'extra ``[icons]``
    active: True per la versione piena (sfondo del colore).
    Per un campo di form con chip modificabili usa il widget
    ``agesci_theme.forms.InputChip``. Stessa firma di ``ag_chip`` del tema
    CoreUI (che ignora ``active``).
    """
    return {
        "label": label,
        "variant": variant,
        "theme": _theme(variant),
        "icona": _icona(icon),
        "icon": _icona(icon, "chip-icon"),
        "active": active,
    }


@register.inclusion_tag("agesci_theme/components/stepper.html")
def ag_stepper(steps=None, current=1, vertical=False):
    """Stepper Bootstrap 6: i passi di un percorso (es. un'iscrizione in più
    fasi), con i passi fatti e quello corrente evidenziati.

    steps: lista di stringhe, oppure di dict con label e url (opzionale: se
    almeno un passo ha url, i passi diventano link).
    current: numero (da 1) del passo corrente; 0 = nessuno.
    vertical: True per l'elenco verticale (default orizzontale, con
    scorrimento se non ci sta).
    """
    passi = []
    for indice, passo in enumerate(steps or [], start=1):
        if isinstance(passo, str):
            passo = {"label": passo}
        passi.append({**passo, "fatto": indice <= current, "corrente": indice == current})
    return {"passi": passi, "con_link": any(p.get("url") for p in passi), "vertical": vertical}


@register.inclusion_tag("agesci_theme/components/carousel.html")
def ag_carousel(items=None, id="", indicators=True, autoplay=False, interval=5000, fade=False):
    """Carousel Bootstrap 6 (scroll-snap) con controlli e indicatori
    sovrapposti alle immagini.

    items: lista di dict con chiavi image_url, alt, title (opz.) e text
    (opz.): title/text compaiono in una didascalia sulla parte bassa.
    autoplay: scorre da solo ogni ``interval`` ms e mostra il pulsante
    pausa/riproduci (obbligatorio per l'accessibilità, WCAG 2.2.2).
    fade: dissolvenza invece dello scorrimento.
    """
    return {
        "items": items or [],
        "id": id or _id_univoco("ag-carousel"),
        "indicators": indicators,
        "autoplay": autoplay,
        "interval": interval,
        "fade": fade,
    }

# django-agesci-theme

[![build](https://github.com/AGESCI-Campania/django-agesci-campania-theme/actions/workflows/build.yml/badge.svg)](https://github.com/AGESCI-Campania/django-agesci-campania-theme/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0%2B-092E20.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3.svg?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![uv](https://img.shields.io/badge/packaged%20with-uv-DE5FE9.svg?logo=uv&logoColor=white)](https://github.com/astral-sh/uv)
[![Version](https://img.shields.io/badge/version-2.1.0-informational.svg)](pyproject.toml)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Tema **Bootstrap 5** riusabile per le applicazioni **Django** dell'**AGESCI Campania**.

Fornisce un `base.html` pronto all'uso con **header a due barre** (barra brand
+ barra ricerca/azioni), **sidebar collapsible**, footer ridisegnato e una
libreria di **componenti opzionali** (`ag_hero`, `ag_feature_grid`,
`ag_jumbotron` e altri 8). Tutto brandizzato con la palette ufficiale del
*Manuale Immagine Coordinata AGESCI 2011* e con la **personalizzazione per
branca** tramite un singolo parametro.

| Ambito | Colore dominante | `data-branca` |
|---|---|---|
| Generico (default) | Blu/Azzurro | `generico` |
| Capi / Comunità Capi | Viola | `capi` |
| Lupetti/Coccinelle (L/C) | Giallo | `lc` |
| Esploratori/Guide (E/G) | Verde | `eg` |
| Rover/Scolte (R/S) | Rosso | `rs` |

Il colore viene applicato rimappando le *CSS custom properties* di Bootstrap, in
funzione dell'attributo `data-branca` sul tag `<html>`. Nessun ricompilo
necessario: basta cambiare una setting.

---

## Installazione

Il pacchetto è disponibile su [PyPI](https://pypi.org/project/django-agesci-campania-theme/).

### Con uv (consigliato)

```bash
uv add django-agesci-campania-theme
```

### Con pip

```bash
pip install django-agesci-campania-theme
```

### Da GitHub (ultima versione non rilasciata)

```bash
uv add "git+https://github.com/AGESCI-Campania/django-agesci-campania-theme.git"
pip install "git+https://github.com/AGESCI-Campania/django-agesci-campania-theme.git"
```

## Configurazione

In `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    "agesci_theme",
]

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            # ... quelli di default ...
            "agesci_theme.context_processors.agesci_theme",
        ],
    },
}]

# --- Personalizzazione tema (tutte opzionali) ---
AGESCI_THEME_BRANCA = "eg"            # generico | capi | lc | eg | rs | viola
AGESCI_THEME_NOME = "Zona Vesuvio"     # mostrato in navbar/footer/title
# Navbar con testo scuro: utile per branca chiara (es. lc = giallo)
AGESCI_THEME_NAVBAR_TESTO_SCURO = False

# Loghi/favicon personalizzati (path relativi a STATIC).
# Se omessi usano gli asset AGESCI Campania inclusi nel pacchetto.
# AGESCI_THEME_LOGO_NAVBAR = "mia_app/img/logo_zona.svg"
# AGESCI_THEME_FAVICON_32 = "mia_app/img/favicon32.png"
```

Assicurati di avere lo static configurato:

```python
STATIC_URL = "static/"
# in produzione:  python manage.py collectstatic
```

## Uso nei template

```django
{% extends "agesci_theme/base.html" %}
{% load agesci_tags %}
{% load agesci_components %}

{% block title %}Home — {{ agesci_theme_nome }}{% endblock %}

{# Nav desktop: icona sopra + etichetta sotto #}
{% block header_nav %}
  <li>
    <a href="/" class="nav-link active">
      <span class="ag-nav-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 16 16">
          <path d="M8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4.5v-5h3v5H14a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354z"/>
        </svg>
      </span>
      Home
    </a>
  </li>
{% endblock %}

{# Nav mobile (offcanvas) #}
{% block offcanvas_nav %}
  <li><a href="/" class="nav-link active">Home</a></li>
{% endblock %}

{% block content %}
  {% ag_hero title="Benvenuti!" subtitle="Il tema AGESCI è operativo."
             cta_text="Scopri di più" cta_url="/chi-siamo/" %}

  <button class="btn btn-primary">Pulsante in colore branca</button>

  {# Emblema di una Zona Campania #}
  {% emblema_zona "vesuvio" css_class="img-fluid" %}

  {# Badge che segue il colore della branca corrente #}
  <span class="badge {% branca_bg %}">Branca</span>
{% endblock %}
```

### Blocchi disponibili in `base.html`

| Blocco | Posizione |
|---|---|
| `title` | `<title>` della pagina |
| `extra_head` | fine `<head>` |
| `header` | intera testata (sostituzione completa) |
| `brand_url` | URL brand nella barra superiore |
| `brand_text` | testo brand nella barra superiore |
| `header_nav` | nav desktop con icone (solo ≥ lg) |
| `offcanvas_nav` | nav mobile nel pannello offcanvas |
| `header_search` | campo ricerca in barra inferiore |
| `header_actions` | pulsanti azione in barra inferiore |
| `sidebar` | sidebar collapsible (vuota = assente) |
| `sidebar_items` | voci `<li>` della sidebar |
| `main_class` | classi CSS del `<main>` (default: `container py-4`) |
| `messages` | messaggi Django (alert Bootstrap) |
| `content` | **contenuto principale** |
| `footer` | footer (sostituzione completa) |
| `footer_brand_text` | testo sotto il logo nel footer |
| `footer_col1_title` / `footer_col2_title` | titoli colonne link |
| `footer_col1_links` / `footer_col2_links` | voci `<li>` colonne link |
| `footer_text` | testo centrale footer (compat. v1) |
| `footer_copyright` | riga copyright |
| `footer_links` | link legali (privacy, ecc.) |
| `extra_js` | script prima di `</body>` |

### Layout applicazione (viewport fisso)

Da ≥ 992 px il `base.html` applica `body { height: 100vh; overflow: hidden }` e
`.ag-scroll-area { min-height: 0; overflow-y: auto }` tramite il CSS del tema.
Il risultato è un layout a **viewport fisso**: header e sidebar fissi; solo
`.ag-scroll-area` (che contiene `<main>` + `<footer>` come fratelli) scorre.
Il footer occupa tutta la larghezza dell'area (viewport − sidebar),
indipendentemente dal `max-width` del `.container` di `<main>`.
Su mobile/tablet (< 992 px) il layout torna al flusso normale.

### Breadcrumb

Passa `breadcrumb_items` dal contesto della view: la breadcrumb compare
automaticamente nella barra inferiore dell'header al posto di ricerca/azioni.

```python
# views.py
def my_view(request):
    return render(request, "mia_app/pagina.html", {
        "breadcrumb_items": [
            {"label": "Home",     "url": "/"},
            {"label": "Sezione",  "url": "/sezione/"},
            {"label": "Pagina corrente"},   # ultimo: active, senza url
        ]
    })
```

In alternativa usa `{% ag_breadcrumb items=breadcrumb_items %}` nel blocco `content`.

### Icone Bootstrap (opzionale)

Supporto tramite [`django-bootstrap-icons`](https://pypi.org/project/django-bootstrap-icons/).
Installazione con l'extra `icons`:

```bash
uv add "django-agesci-campania-theme[icons]"
# oppure
pip install "django-agesci-campania-theme[icons]"
```

Aggiungi in `settings.py`:

```python
INSTALLED_APPS = [..., "agesci_theme", "django_bootstrap_icons"]

# Consigliato: abilita la cache per non scaricare gli SVG a ogni richiesta
BS_ICONS_CACHE = BASE_DIR / ".bs-icons-cache"
```

Uso nei template:

```django
{% load bootstrap_icons %}
{% bs_icon "house" %}
{% bs_icon "calendar-event" size="1.5em" %}
```

### Template tag

**`{% load agesci_tags %}`**

- `{% emblema_zona "napoli" css_class="..." alt="..." %}` — `<img>` dell'emblema di Zona.
- `{% zone_disponibili %}` — lista delle chiavi di zona.
- `{% branca_bg %}` — classe CSS di sfondo nel colore della branca corrente.

Zone disponibili: `caserta, faito, felix, hirpinia, liternum, napoli,
poseidonia, salerno, samnium, vesuvio, volturno`.

**`{% load agesci_components %}`**

11 componenti UI opzionali: `{% ag_hero %}`, `{% ag_feature_card %}`,
`{% ag_feature_grid %}`, `{% ag_jumbotron %}`, `{% ag_badge %}`,
`{% ag_button %}`, `{% ag_breadcrumb %}`, `{% ag_dropdown %}`,
`{% ag_list_group %}`, `{% ag_modal_trigger %}`, `{% ag_masonry_grid %}`.

I template sono in `agesci_theme/components/` e sono sovrascrivibili.
Vedi la [documentazione completa](https://django-agesci-campania-theme.readthedocs.io/).

## Classi utility palette

`bg-ag-viola`, `bg-ag-azzurro`, `bg-ag-giallo-lc`, `bg-ag-verde-eg`,
`bg-ag-rosso-rs`, `bg-ag-giallo-oro` e i corrispettivi `text-ag-*`.

---

## Progetto demo

Il repository include un progetto Django di esempio che mostra header, sidebar,
footer, componenti opzionali (`/components/`), palette e zone. Per avviarlo:

```bash
# 1. Clona il repository e installa le dipendenze (crea .venv automaticamente)
git clone https://github.com/AGESCI-Campania/django-agesci-campania-theme.git
cd django-agesci-campania-theme
uv sync

# 2. Crea il database e avvia il server
uv run python example_project/manage.py migrate
uv run python example_project/manage.py runserver
```

Apri `http://127.0.0.1:8000/` nel browser.

Per provare le diverse branche modifica `AGESCI_THEME_BRANCA` in
`example_project/config/settings.py` (`generico`, `capi`, `lc`, `eg`, `rs`)
e ricarica la pagina — nessun ricompilo necessario.

---

## Sviluppo del tema (modificare i colori/SCSS)

Il CSS compilato è già committato, quindi **chi installa il pacchetto non ha
bisogno di Sass**. Serve solo se vuoi modificare lo SCSS.

```bash
npm install
npm run build:css      # rigenera agesci.css e agesci.min.css
npm run watch:css      # ricompila live durante lo sviluppo
```

I sorgenti sono in `agesci_theme/static/agesci_theme/scss/`:
`_palette.scss`, `_branche.scss`, `_bootstrap-overrides.scss`,
`_header.scss`, `_sidebar.scss`, `_footer.scss`, `_components.scss`.

## Palette ufficiale

Estratta dal *Manuale Immagine Coordinata AGESCI 2011*, sez. 7.

| Colore | Pantone | HEX |
|---|---|---|
| Viola | 527C | `#7A1E99` |
| Viola scuro | 072C | `#622599` |
| Giallo oro | 123C | `#FFCC1E` |
| Azzurro | 279C | `#6689CC` |
| Giallo L/C | 109C | `#F9D616` |
| Verde E/G | 363C | `#3D8E33` |
| Rosso R/S | 032C | `#EF3340` * |

\* Il manuale 2011 riporta per il 032C un RGB anomalo (refuso di stampa,
confermato): è stato adottato lo standard Pantone 032C. Vedi `_palette.scss`.

## Licenza

Codice sotto licenza MIT. Marchi, emblemi e palette AGESCI restano proprietà
dell'Associazione e sono soggetti al regolamento associativo sull'uso del marchio.

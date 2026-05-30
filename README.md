# django-agesci-theme

[![build](https://github.com/AGESCI-Campania/django-agesci-campania-theme/actions/workflows/build.yml/badge.svg)](https://github.com/AGESCI-Campania/django-agesci-campania-theme/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0%2B-092E20.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3.svg?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![uv](https://img.shields.io/badge/packaged%20with-uv-DE5FE9.svg?logo=uv&logoColor=white)](https://github.com/astral-sh/uv)
[![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](pyproject.toml)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Tema **Bootstrap 5** riusabile per le applicazioni **Django** dell'**AGESCI Campania**.

Fornisce un `base.html` pronto all'uso, navbar e footer brandizzati, la palette
ufficiale del *Manuale Immagine Coordinata AGESCI 2011*, gli emblemi associativi
e regionali, e la **personalizzazione per branca** tramite un singolo parametro.

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

Il pacchetto si installa direttamente da GitHub.

### Con uv (consigliato)

```bash
uv add "git+https://github.com/AGESCI-Campania/django-agesci-campania-theme.git"
```

### Con pip

```bash
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

{% block title %}Home — {{ agesci_theme_nome }}{% endblock %}

{% block nav_items %}
  <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
  <li class="nav-item"><a class="nav-link" href="/eventi/">Eventi</a></li>
{% endblock %}

{% block content %}
  <h1>Benvenuti</h1>
  <button class="btn btn-primary">Pulsante in colore branca</button>

  {# Emblema di una Zona Campania #}
  {% emblema_zona "vesuvio" css_class="img-fluid" %}

  {# Badge che segue il colore della branca corrente #}
  <span class="badge {% branca_bg %}">Branca</span>
{% endblock %}
```

### Blocchi disponibili in `base.html`

`title`, `extra_head`, `navbar`, `brand_url`, `brand_text`, `nav_items`,
`main_class`, `messages`, `content`, `footer`, `footer_text`, `footer_links`,
`extra_js`.

### Template tag (`{% load agesci_tags %}`)

- `{% emblema_zona "napoli" css_class="..." alt="..." %}` — `<img>` dell'emblema di Zona.
- `{% zone_disponibili %}` — lista delle chiavi di zona.
- `{% branca_bg %}` — classe CSS di sfondo nel colore della branca corrente.

Zone disponibili: `caserta, faito, felix, hirpinia, liternum, napoli,
poseidonia, salerno, samnium, vesuvio, volturno`.

## Classi utility palette

`bg-ag-viola`, `bg-ag-azzurro`, `bg-ag-giallo-lc`, `bg-ag-verde-eg`,
`bg-ag-rosso-rs`, `bg-ag-giallo-oro` e i corrispettivi `text-ag-*`.

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
`_palette.scss` (colori del manuale), `_branche.scss` (mappa ambiti→colore),
`_bootstrap-overrides.scss` (componenti).

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

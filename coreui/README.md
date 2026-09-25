# django-agesci-campania-coreui-theme

[![build](https://github.com/AGESCI-Campania/django-agesci-campania-theme/actions/workflows/build.yml/badge.svg)](https://github.com/AGESCI-Campania/django-agesci-campania-theme/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0%2B-092E20.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![CoreUI](https://img.shields.io/badge/CoreUI-5-3399FF.svg)](https://coreui.io/bootstrap/)
[![uv](https://img.shields.io/badge/packaged%20with-uv-DE5FE9.svg?logo=uv&logoColor=white)](https://github.com/astral-sh/uv)
[![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](pyproject.toml)

Tema **CoreUI 5** (versione free, MIT) per le applicazioni **Django**
dell'**AGESCI Campania**.

Estende [`django-agesci-campania-theme`](https://pypi.org/project/django-agesci-campania-theme/)
(installato automaticamente come dipendenza), da cui riusa palette ufficiale,
colore per branca, form renderer, override di django-allauth e template tag.
In più fornisce:

- un `base.html` con il **layout nativo CoreUI**: sidebar fissa e
  comprimibile, overlay su mobile, header sticky con breadcrumb;
- i **componenti free di CoreUI** colorati per branca: `{% ag_callout %}`,
  `{% ag_avatar %}`, `{% ag_chip %}`, `{% ag_nav_item %}`, `{% ag_nav_title %}`;
- il widget di form **`InputChip`** / campo **`CampoChip`** (chip-input di CoreUI).

I componenti **PRO** di CoreUI (date picker, multi select, ecc.) non sono
inclusi: richiedono una licenza commerciale.

## Installazione

```bash
uv add django-agesci-campania-coreui-theme
```

```python
INSTALLED_APPS = [
    ...,
    "agesci_coreui",
    "agesci_theme",   # obbligatoria: il tema CoreUI estende il tema base
    ...,
]

TEMPLATES = [{"OPTIONS": {"context_processors": [
    ...,
    "agesci_theme.context_processors.agesci_theme",
]}}]
```

Le stesse settings `AGESCI_THEME_*` (branca, nome, loghi, favicon) e
l'opzionale `FORM_RENDERER = "agesci_theme.forms.AgesciFormRenderer"` del
tema base restano valide.

## Uso nei template

Il `templates/base.html` del progetto estende il layout CoreUI (serve anche
alle pagine allauth, che estendono letteralmente `"base.html"`):

```django
{% extends "agesci_coreui/base.html" %}
{% load agesci_coreui %}
{% load agesci_tags %}

{% block sidebar_items %}
  {% ag_nav_title "Gestione" %}
  {% ag_nav_item "Home" "/" icon="house-fill" %}
  {% ag_nav_item "Iscrizioni" "/iscrizioni/" icon="people-fill" badge="3" %}
{% endblock %}

{% block header_nav %}
  <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
{% endblock %}

{% block content %}
  {% ag_callout title="Attenzione" text="Le iscrizioni chiudono venerdì." variant="warning" %}
  {% ag_avatar name="Mario Rossi" status="success" %}
  {% ag_chip "E/G" variant="success" %}

  {# Badge che segue il colore della branca corrente #}
  <span class="badge {% branca_bg %}">Branca</span>
{% endblock %}
```

`variant="primary"` (callout, chip) segue sempre il colore della branca.
Tutti i componenti opzionali del tema base (`ag_hero`, `ag_feature_grid`,
`ag_dropdown`, `ag_modal_trigger`, `ag_password_field`,
`ag_multiselect_dropdown`, ecc.) funzionano invariati: scrivono
`data-coreui-*` invece di `data-bs-*` grazie a `{% ag_js %}`.

### Chip-input nei form

```python
from agesci_coreui.forms import CampoChip, InputChip

class EventoForm(forms.Form):
    tag = CampoChip(
        required=False,
        max_chip=5,
        widget=InputChip(placeholder="Scrivi e premi Invio…"),
    )
```

`CampoChip` restituisce una lista di stringhe (`cleaned_data["tag"]`); non
richiede `AgesciFormRenderer`.

## Progetto demo

**Demo online:** <https://agesci-campania.github.io/django-agesci-campania-theme/coreui/> (statica: l'invio dei form è disattivato).

Il repository include una variante CoreUI del progetto Django di esempio,
con lo stesso demo form (compreso il campo `CampoChip`):

```bash
git clone https://github.com/AGESCI-Campania/django-agesci-campania-theme.git
cd django-agesci-campania-theme
uv sync
uv run python example_project/manage.py migrate
uv run python example_project/manage.py runserver --settings=config.settings_coreui
```

Apri `http://127.0.0.1:8000/`.

## Documentazione completa

[Tema CoreUI](https://django-agesci-campania-theme.readthedocs.io/it/latest/coreui.html)
sul sito della documentazione, o [`docs/coreui.md`](../docs/coreui.md) nel
repository. Il tema base è documentato nel
[README principale](https://github.com/AGESCI-Campania/django-agesci-campania-theme#readme)
e sul [sito della documentazione](https://django-agesci-campania-theme.readthedocs.io/).

## Licenza

Codice sotto licenza MIT. Marchi, emblemi e palette AGESCI restano proprietà
dell'Associazione e sono soggetti al regolamento associativo sull'uso del
marchio. CoreUI è un marchio dei rispettivi autori; questo pacchetto usa
solo la variante free (licenza MIT).

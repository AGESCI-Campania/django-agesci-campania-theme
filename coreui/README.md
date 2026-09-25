# django-agesci-campania-coreui-theme

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

Il `templates/base.html` del progetto estende il layout CoreUI:

```django
{% extends "agesci_coreui/base.html" %}
```

Documentazione completa: `docs/coreui.md` nel repository.

# Installazione

## Requisiti

- Python **3.12** o superiore
- Django **6.0** o superiore
- Bootstrap **5.3** (caricato da CDN, non serve installarlo)

---

## Da PyPI (consigliato)

Il pacchetto è pubblicato su [PyPI](https://pypi.org/project/django-agesci-campania-theme/).

::::{tab-set}

:::{tab-item} uv (consigliato)
```bash
uv add django-agesci-campania-theme
```
:::

:::{tab-item} pip
```bash
pip install django-agesci-campania-theme
```
:::

::::

## Con il supporto icone Bootstrap

Il supporto a [Bootstrap Icons](https://icons.getbootstrap.com/) via
[django-bootstrap-icons](https://pypi.org/project/django-bootstrap-icons/)
è incluso come dipendenza opzionale nell'extra `[icons]`:

```bash
# uv
uv add "django-agesci-campania-theme[icons]"

# pip
pip install "django-agesci-campania-theme[icons]"
```

Vedi la sezione [Icone Bootstrap](componenti.md#icone-bootstrap) per la configurazione.

## Con il supporto form Bootstrap 5 e django-allauth

Lo styling Bootstrap 5 dei form Django (`is-invalid`/`invalid-feedback`,
toggle mostra/nascondi password) e degli override per
[django-allauth](https://docs.allauth.org/) sono **inclusi nel tema**, senza
dipendenze aggiuntive — vanno solo attivati esplicitamente, vedi
[Form e validazione](forms.md). L'extra `[allauth]` è solo per
documentazione/test (pinna la versione testata):

```bash
uv add "django-agesci-campania-theme[allauth]"
```

Vedi [Integrazione con django-allauth](allauth.md) per l'attivazione completa.

---

## Da GitHub (versione di sviluppo)

Per installare l'ultima versione dal branch `main` (serie 2.x attuale):

```bash
# uv
uv add "git+https://github.com/AGESCI-Campania/django-agesci-campania-theme.git"

# pip
pip install "git+https://github.com/AGESCI-Campania/django-agesci-campania-theme.git"
```

:::{note}
La serie 2.x introduce **breaking changes** rispetto alla v1.x. Consulta la
[guida di migrazione](template.md#migrazione-dalla-v1x) prima di aggiornare
da una versione 1.x.
:::

---

## Configurazione minima in Django

Dopo l'installazione aggiungi `"agesci_theme"` a `INSTALLED_APPS` e il context
processor alla lista dei `context_processors`:

```python
# settings.py

INSTALLED_APPS = [
    # ... app Django standard ...
    "agesci_theme",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # --- Tema AGESCI ---
                "agesci_theme.context_processors.agesci_theme",
            ],
        },
    }
]
```

Assicurati che Django possa servire i file statici:

```python
STATIC_URL = "static/"
# In produzione esegui: python manage.py collectstatic
```

Il tema è ora pronto. Procedi con la [Configurazione](configurazione.md) per
personalizzarlo.

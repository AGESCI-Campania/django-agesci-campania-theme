# Avvio rapido

Questa guida mostra i passi minimi per avere un'applicazione Django con il tema
AGESCI operativo in meno di cinque minuti.

---

## 1. Installa il pacchetto

```bash
uv add django-agesci-campania-theme
```

## 2. Aggiorna `settings.py`

```python
INSTALLED_APPS = [
    # ... app esistenti ...
    "agesci_theme",
]

TEMPLATES = [{
    # ...
    "OPTIONS": {
        "context_processors": [
            # ... context processor esistenti ...
            "agesci_theme.context_processors.agesci_theme",
        ],
    },
}]

# Opzionale: personalizza branca e nome
AGESCI_THEME_BRANCA = "eg"
AGESCI_THEME_NOME   = "La mia app scout"
```

## 3. Crea il primo template

```django
{# mia_app/templates/mia_app/home.html #}
{% extends "agesci_theme/base.html" %}

{% block title %}Home — {{ agesci_theme_nome }}{% endblock %}

{% block nav_items %}
  <li class="nav-item">
    <a class="nav-link active" href="/">Home</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="/eventi/">Eventi</a>
  </li>
{% endblock %}

{% block content %}
  <h1>Benvenuti!</h1>
  <p class="lead">Il tema AGESCI è operativo.</p>
  <a href="/eventi/" class="btn btn-primary">Vai agli eventi</a>
{% endblock %}
```

## 4. Avvia il server

```bash
python manage.py runserver
```

Apri `http://127.0.0.1:8000/` nel browser: la navbar, il footer e i colori della
branca selezionata sono già attivi.

---

## Passo successivo

- Cambia branca in `settings.py` e ricarica la pagina: i colori si aggiornano
  senza nessun ricompilo.
- Aggiungi una [breadcrumb](componenti.md#breadcrumb) passando `breadcrumb_items`
  dalla view.
- Scopri tutti i [blocchi disponibili](template.md) per personalizzare navbar,
  footer e layout.
- Prova il [progetto demo](quickstart.md#progetto-demo) incluso nel repository per vedere
  tutti i componenti in azione.

---

(progetto-demo)=
## Progetto demo

Il repository include un progetto Django completo che mostra navbar, breadcrumb,
sub-navbar, footer, palette e zone:

```bash
git clone https://github.com/AGESCI-Campania/django-agesci-campania-theme.git
cd django-agesci-campania-theme
uv sync
uv run python example_project/manage.py migrate
uv run python example_project/manage.py runserver
```

Modifica `AGESCI_THEME_BRANCA` in `example_project/config/settings.py` per
vedere il cambio di colore in tempo reale.

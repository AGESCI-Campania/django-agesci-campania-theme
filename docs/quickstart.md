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
  <li>
    <a href="/eventi/" class="nav-link">
      <span class="ag-nav-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 16 16">
          <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5"/>
        </svg>
      </span>
      Eventi
    </a>
  </li>
{% endblock %}

{# Ricerca nella barra inferiore #}
{% block header_search %}
  <form class="col-12 col-lg-auto me-lg-auto" role="search">
    <input type="search" class="form-control" placeholder="Cerca..." aria-label="Cerca">
  </form>
{% endblock %}

{# Pulsanti nella barra inferiore #}
{% block header_actions %}
  <a href="/login/" class="btn btn-light text-dark">Accedi</a>
  <a href="/register/" class="btn btn-primary">Registrati</a>
{% endblock %}

{# Nav mobile (offcanvas) #}
{% block offcanvas_nav %}
  <li><a href="/" class="nav-link active">Home</a></li>
  <li><a href="/eventi/" class="nav-link">Eventi</a></li>
{% endblock %}

{# Footer #}
{% block footer_col1_title %}Sezioni{% endblock %}
{% block footer_col1_links %}
  <li><a href="/eventi/">Eventi</a></li>
  <li><a href="/chi-siamo/">Chi siamo</a></li>
{% endblock %}

{% block content %}
  {% ag_hero title="Benvenuti!" subtitle="Il tema AGESCI è operativo." cta_text="Scopri di più" cta_url="/chi-siamo/" %}

  <h2 class="mt-4">Contenuto della pagina</h2>
  <p>Inizia a costruire la tua app scout.</p>
  <a href="/eventi/" class="btn btn-primary">Vai agli eventi</a>
{% endblock %}
```

## 4. Avvia il server

```bash
python manage.py runserver
```

Apri `http://127.0.0.1:8000/` nel browser: l'header a due barre, il footer
e i colori della branca selezionata sono già attivi.

---

## Passo successivo

- Cambia branca in `settings.py` e ricarica: i colori si aggiornano senza
  ricompilare nulla.
- Aggiungi una sidebar sovrascrivendo il blocco `sidebar`
  (vedi [Sidebar](componenti.md#sidebar)).
- Usa i componenti opzionali: `{% load agesci_components %}` poi
  `{% ag_hero %}`, `{% ag_feature_grid %}`, `{% ag_jumbotron %}` e altri
  (vedi [Template tag — agesci_components](templatetags.md#agesci-components)).
- Esplora tutti i [blocchi disponibili](template.md) per personalizzare
  header, footer e layout.

---

(progetto-demo)=
## Progetto demo

Il repository include un progetto Django completo che mostra header, sidebar,
footer, palette, componenti e zone:

```bash
git clone -b v2 https://github.com/AGESCI-Campania/django-agesci-campania-theme.git
cd django-agesci-campania-theme
uv sync
uv run python example_project/manage.py migrate
uv run python example_project/manage.py runserver
```

Modifica `AGESCI_THEME_BRANCA` in `example_project/config/settings.py` per
vedere il cambio di colore in tempo reale.

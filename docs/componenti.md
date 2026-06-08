# Componenti UI

## Navbar

La navbar è inclusa automaticamente da `base.html`. Il suo colore di sfondo
segue `--ag-primary` (cioè la branca impostata) e si adatta senza alcuna
modifica CSS.

### Personalizzazione via blocchi

```django
{% extends "agesci_theme/base.html" %}

{% block brand_url %}{% url 'home' %}{% endblock %}
{% block brand_text %}Zona Vesuvio{% endblock %}

{% block nav_items %}
  <li class="nav-item">
    <a class="nav-link active" href="/">Home</a>
  </li>
  <li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">
      Sezioni
    </a>
    <ul class="dropdown-menu">
      <li><a class="dropdown-item" href="/eventi/">Eventi</a></li>
      <li><a class="dropdown-item" href="/documenti/">Documenti</a></li>
    </ul>
  </li>
{% endblock %}
```

### Navbar con testo scuro

Per le branche a colore chiaro (es. `lc` = giallo) il testo bianco è
illeggibile. Imposta in `settings.py`:

```python
AGESCI_THEME_NAVBAR_TESTO_SCURO = True
```

Questo aggiunge la classe `.text-dark` alla navbar, che sovrascrive
automaticamente tutti i colori dei link.

---

(breadcrumb)=
## Breadcrumb

La breadcrumb appare sotto la navbar quando viene passata la variabile di
contesto `breadcrumb_items` dalla view. Se la variabile è assente o vuota il
blocco non viene renderizzato.

### Uso dalla view

```python
# views.py
def dettaglio_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, "eventi/dettaglio.html", {
        "evento": evento,
        "breadcrumb_items": [
            {"label": "Home",    "url": "/"},
            {"label": "Eventi",  "url": "/eventi/"},
            {"label": evento.titolo, "url": ""},   # stringa vuota = elemento attivo
        ],
    })
```

L'ultimo elemento con `url` vuota viene automaticamente marcato come `active`
e non genera un link.

### Struttura di `breadcrumb_items`

```python
breadcrumb_items = [
    {"label": "Testo del link", "url": "/percorso/"},  # elemento con link
    {"label": "Pagina corrente", "url": ""},            # elemento attivo (no link)
]
```

### Override del blocco

Se hai esigenze particolari puoi sovrascrivere il blocco nel template:

```django
{% block breadcrumb %}
  <nav aria-label="percorso" class="breadcrumb-agesci px-3 py-2">
    <ol class="breadcrumb mb-0">
      <li class="breadcrumb-item"><a href="/">Home</a></li>
      <li class="breadcrumb-item active">Pagina custom</li>
    </ol>
  </nav>
{% endblock %}
```

---

(sub-navbar)=
## Sub-navbar

La sub-navbar è una barra di navigazione secondaria con pill colorate secondo
la branca. Appare tra la breadcrumb e il contenuto principale.

### Uso dalla view

```python
# views.py
def sezione(request):
    return render(request, "mia_app/sezione.html", {
        "subnav_items": [
            {"label": "Panoramica", "url": "/sezione/",         "active": True},
            {"label": "Elenco",     "url": "/sezione/lista/",   "active": False},
            {"label": "Impostazioni", "url": "/sezione/impostazioni/", "active": False},
        ],
    })
```

### Struttura di `subnav_items`

```python
subnav_items = [
    {
        "label":  "Testo voce",    # obbligatorio
        "url":    "/percorso/",    # obbligatorio
        "active": True,            # True per la voce corrente
    },
    ...
]
```

La voce con `"active": True` riceve la classe `.active` della pill colorata
nel colore della branca.

---

## Footer

Il footer è incluso automaticamente. Mostra:

- **Sinistra:** logo navbar o emblema.
- **Centro:** nome dell'app (`AGESCI_THEME_NOME`) e testo personalizzabile.
- **Destra:** colonna link.

### Personalizzazione via blocchi

```django
{% block footer_text %}
  <p class="mb-1 fw-semibold">Zona Vesuvio</p>
  <p class="mb-0 small opacity-75">AGESCI Campania — Regione Campania</p>
{% endblock %}

{% block footer_links %}
  <ul class="list-unstyled mb-0 small">
    <li><a href="/privacy/">Privacy Policy</a></li>
    <li><a href="/accessibilita/">Accessibilità</a></li>
    <li><a href="mailto:zona@esempio.it">Contatti</a></li>
  </ul>
{% endblock %}
```

---

## Messaggi Django

Il blocco `messages` converte automaticamente i messaggi del framework di
messaggistica di Django in alert Bootstrap 5 con pulsante di chiusura:

```python
# views.py
from django.contrib import messages

def mia_view(request):
    messages.success(request, "Operazione completata con successo.")
    messages.warning(request, "Attenzione: l'evento è quasi pieno.")
    return redirect("home")
```

Il tag del messaggio (`success`, `warning`, `error`, `info`) viene usato come
classe Bootstrap dell'alert (`alert-success`, `alert-warning`, ecc.).

---

(icone-bootstrap)=
## Icone Bootstrap

Il supporto a [Bootstrap Icons](https://icons.getbootstrap.com/) è disponibile
come dipendenza opzionale tramite
[django-bootstrap-icons](https://pypi.org/project/django-bootstrap-icons/).

### Installazione

```bash
uv add "django-agesci-campania-theme[icons]"
```

### Configurazione

```python
INSTALLED_APPS = [
    # ...
    "agesci_theme",
    "django_bootstrap_icons",  # deve seguire agesci_theme
]

# Consigliato: cache locale degli SVG per evitare richieste HTTP a ogni render
BS_ICONS_CACHE = BASE_DIR / ".bs-icons-cache"
```

### Uso nei template

```django
{% load bootstrap_icons %}

{# Icona inline SVG #}
{% bs_icon "house" %}
{% bs_icon "calendar-event" %}
{% bs_icon "person-circle" size="1.5em" %}
{% bs_icon "gear" class="text-primary" extra_attrs='aria-hidden="true"' %}
```

Vedi la [libreria completa delle icone](https://icons.getbootstrap.com/) per
i nomi disponibili.

---

## Pulsanti e componenti Bootstrap

Tutti i componenti Bootstrap che usano il colore `primary` ereditano
automaticamente il colore della branca. Non occorre nessuna classe aggiuntiva:

```django
<button class="btn btn-primary">Pulsante branca</button>
<button class="btn btn-outline-primary">Outline</button>
<span class="badge text-bg-primary">Badge</span>
<div class="alert alert-primary">Alert</div>
<div class="progress-bar bg-primary" style="width: 60%"></div>
```

Questo funziona grazie alla rimappatura automatica di `--bs-primary` operata
da `_bootstrap-overrides.scss` verso `--ag-primary`.

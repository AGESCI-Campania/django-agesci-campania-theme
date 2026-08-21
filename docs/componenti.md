# Componenti UI

## Header

L'header a due barre è incluso automaticamente da `base.html` tramite
`partials/header.html`. Il colore di sfondo della barra superiore segue
`--ag-primary` (branca impostata).

### Struttura

```
┌─────────────────────────────────────────────────┐
│ [Logo] [NomeApp]   [Nav desktop con icone]  [☰] │  ← ag-header-top (colore branca, full-width)
├─────────────────────────────────────────────────┤
│ [Campo ricerca ────────────────] [Accedi] [Reg] │  ← ag-header-bottom (sfondo chiaro, full-width)
└─────────────────────────────────────────────────┘
```

Entrambe le barre sono **full-width**: il contenuto si estende a tutta la
larghezza del viewport (nessun `<div class="container">` interno). Il padding
laterale `px-3` è applicato direttamente sull'elemento `ag-header-top` /
`ag-header-bottom`.

Su mobile/tablet (< lg) il menu desktop è nascosto: l'hamburger apre un
pannello offcanvas Bootstrap con i link del blocco `offcanvas_nav`.

### Personalizzazione via blocchi

```django
{% extends "agesci_theme/base.html" %}
{% load bootstrap_icons %}

{% block brand_url %}{% url 'home' %}{% endblock %}
{% block brand_text %}Zona Vesuvio{% endblock %}

{# Nav desktop: icona sopra + etichetta sotto #}
{% block header_nav %}
  <li>
    <a href="/" class="nav-link active">
      <span class="ag-nav-icon">{% bs_icon "house-fill" %}</span>
      Home
    </a>
  </li>
  <li>
    <a href="/eventi/" class="nav-link">
      <span class="ag-nav-icon">{% bs_icon "calendar-event" %}</span>
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

{# Pulsanti azione nella barra inferiore #}
{% block header_actions %}
  <a href="{% url 'login' %}" class="btn btn-light text-dark">Accedi</a>
  <a href="{% url 'register' %}" class="btn btn-primary">Registrati</a>
{% endblock %}

{# Nav mobile nel pannello offcanvas #}
{% block offcanvas_nav %}
  <li><a href="/" class="nav-link active">{% bs_icon "house-fill" %} Home</a></li>
  <li><a href="/eventi/" class="nav-link">{% bs_icon "calendar-event" %} Eventi</a></li>
{% endblock %}
```

### Breadcrumb automatica nell'header

Quando la view passa `breadcrumb_items` nel contesto, la barra inferiore
(`ag-header-bottom`) mostra automaticamente la breadcrumb al posto di
`header_search` / `header_actions`:

```python
# views.py
def mia_view(request):
    return render(request, "...", {
        "breadcrumb_items": [
            {"label": "Home",    "url": "/"},
            {"label": "Sezione", "url": "/sezione/"},
            {"label": "Pagina corrente"},   # ultimo elemento: active, nessun url
        ]
    })
```

Se `breadcrumb_items` non è presente nel contesto, la barra inferiore mostra
normalmente `header_search` e `header_actions`. Per posizionare la breadcrumb
manualmente nel corpo della pagina usa invece `{% ag_breadcrumb %}` nel blocco
`content` (vedi [Template tag](templatetags.md#ag-breadcrumb)).

---

(sidebar)=
## Sidebar

La sidebar collapsible è **opzionale**: appare solo quando il blocco `sidebar`
viene popolato. Quando è vuoto (default) il layout rimane a colonna singola.

### Attivazione

```django
{% extends "agesci_theme/base.html" %}

{% block sidebar %}
  {% include "agesci_theme/partials/sidebar.html" with variant="dark" %}
{% endblock %}

{% block sidebar_items %}
  <li>
    <a href="/" class="ag-sidebar__nav-link">
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
        <path d="M8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4.5v-5h3v5H14a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354z"/>
      </svg>
      <span class="ag-sidebar__label">Home</span>
    </a>
  </li>
  <li>
    <a href="/impostazioni/" class="ag-sidebar__nav-link">
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
        <path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492M5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0"/>
        <path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.892 3.433-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.892-1.64-.901-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52z"/>
      </svg>
      <span class="ag-sidebar__label">Impostazioni</span>
    </a>
  </li>
{% endblock %}
```

### Varianti

| `variant` | Sfondo | Uso tipico |
|---|---|---|
| `"dark"` (default) | `var(--ag-primary)` — colore branca | App gestionali, dashboard |
| `"light"` | `#f8f9fa` con bordo | Portali pubblici, app chiare |

### Comportamento collapsibile

Il toggle in cima alla sidebar comprime la barra a sola icona (64 px).
Lo stato viene salvato in `localStorage` con chiave `ag-sidebar-collapsed`,
così viene ricordato tra i refresh della pagina.

### Dropdown utente in fondo alla sidebar

Il partial include di default una sezione `ag-sidebar__user` con avatar a
iniziali circolari, nome e link "Esci". Appare automaticamente quando
`request.user.is_authenticated` è `True`. Quando la sidebar è collassata
rimane visibile solo l'avatar.

Comportamento per variante:

| Variante | Avatar | Bordo superiore |
|---|---|---|
| `dark` | `rgba(0,0,0,.25)` su sfondo primario | `rgba(255,255,255,.15)` |
| `light` | `var(--ag-primary-subtle)` | `var(--bs-border-color)` |

Per personalizzare i link (es. URL di logout) occorre sovrascrivere il blocco
`sidebar` riproducendo la struttura del partial e aggiungendo il blocco
`sidebar_user` personalizzato (vedi [Template e blocchi](template.md#sidebar_user)).

### Titoli di sezione

Per aggiungere separatori tra gruppi di voci usa la classe
`ag-sidebar__section-title`:

```html
<li class="ag-sidebar__section-title">Gestione</li>
<li><a href="..." class="ag-sidebar__nav-link">...</a></li>
```

---

## Footer

Il footer è incluso automaticamente da `base.html`. La struttura di default
ha colonna logo, due colonne link personalizzabili, testo centrale e riga
copyright.

### Personalizzazione via blocchi

```django
{% block footer_brand_text %}Zona Vesuvio — AGESCI Campania{% endblock %}

{% block footer_col1_title %}Associazione{% endblock %}
{% block footer_col1_links %}
  <li><a href="/chi-siamo/">Chi siamo</a></li>
  <li><a href="/branche/">Le branche</a></li>
  <li><a href="/zone/">Zone</a></li>
{% endblock %}

{% block footer_col2_title %}Risorse{% endblock %}
{% block footer_col2_links %}
  <li><a href="https://www.agesci.it" target="_blank" rel="noopener">agesci.it</a></li>
  <li><a href="/documenti/">Documenti</a></li>
{% endblock %}

{% block footer_text %}
  <strong>{{ agesci_theme_nome }}</strong><br>
  Associazione Guide e Scouts Cattolici Italiani
{% endblock %}

{% block footer_copyright %}© 2025 AGESCI Campania{% endblock %}

{% block footer_links %}
  <li><a href="/privacy/">Privacy</a></li>
  <li><a href="/accessibilita/">Accessibilità</a></li>
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
    "django_bootstrap_icons",
]

BS_ICONS_CACHE = BASE_DIR / ".bs-icons-cache"
```

### Uso nei template

```django
{% load bootstrap_icons %}

{% bs_icon "house" %}
{% bs_icon "calendar-event" %}
{% bs_icon "person-circle" size="1.5em" %}
{% bs_icon "gear" class="text-primary" extra_attrs='aria-hidden="true"' %}
```

---

## Componenti opzionali

I componenti opzionali si caricano con:

```django
{% load agesci_components %}
```

Tutti usano `inclusion_tag` con template in `agesci_theme/components/`:
sono sovrascrivibili creando un file con lo stesso percorso nel progetto figlio.

Tra questi, `{% ag_password_field %}` è un campo password con pulsante
mostra/nascondi, utilizzabile in qualsiasi form scritto a mano — vedi
[Form e validazione](forms.md#il-componente-ag-password-field).

Vedi [Template tag — agesci_components](templatetags.md#agesci-components)
per la documentazione completa di ogni tag.

---

## Pulsanti e componenti Bootstrap nativi

Tutti i componenti Bootstrap che usano il colore `primary` ereditano
automaticamente il colore della branca. Non occorre nessuna classe aggiuntiva:

```django
<button class="btn btn-primary">Pulsante branca</button>
<button class="btn btn-outline-primary">Outline</button>
<span class="badge text-bg-primary">Badge</span>
<div class="alert alert-primary">Alert</div>
```

Questo funziona grazie alla rimappatura automatica di `--bs-primary` verso
`--ag-primary` operata da `_bootstrap-overrides.scss`.

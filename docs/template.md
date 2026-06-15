# Template e blocchi

## Ereditare `base.html`

Tutti i template della tua applicazione devono estendere il base template del tema:

```django
{% extends "agesci_theme/base.html" %}
```

Il `base.html` carica automaticamente Bootstrap 5 (via CDN), i font del Manuale
Immagine Coordinata (Montserrat e Open Sans), il CSS del tema AGESCI e i partial
di header e footer.

---

## Struttura HTML generata

```
<html data-branca="...">
  <head>
    Bootstrap CSS · Font · agesci.min.css · [extra_head]
  </head>
  <body class="d-flex flex-column">
    [header]                         ← barra superiore + barra inferiore + offcanvas
    <div class="d-flex flex-grow-1 overflow-hidden">
      [sidebar]                      ← vuoto di default; attivare con il blocco sidebar
      <div class="ag-scroll-area flex-grow-1">
        <main class="[main_class]">
          [messages]
          [content]
        </main>
        [footer]                     ← larghezza completa (non vincolata da .container)
      </div>
    </div>
    Bootstrap JS · [extra_js]
  </body>
</html>
```

---

## Blocchi dell'header

### `header`

Sostituisce l'intera testata (entrambe le barre + offcanvas). Normalmente non
si sovrascrive questo blocco: si usano i sotto-blocchi specifici.

```django
{% block header %}
  {# testata completamente custom #}
{% endblock %}
```

---

### `brand_url`

URL cliccabile del brand nella barra superiore. Default: `/`.

```django
{% block brand_url %}{% url 'home' %}{% endblock %}
```

---

### `brand_text`

Testo mostrato accanto al logo nella barra superiore. Default: `agesci_theme_nome`.

```django
{% block brand_text %}Zona Vesuvio{% endblock %}
```

---

### `header_nav`

Voci di navigazione nella barra superiore, visibili **solo su desktop** (≥ lg).
Ogni voce è tipicamente un `<li>` con icona centrata sopra e testo sotto,
secondo il pattern Bootstrap "headers":

```django
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
```

La classe `ag-nav-icon` con `display: block` centra l'icona sopra l'etichetta.

---

### `offcanvas_nav`

Voci di navigazione nel pannello offcanvas, visibili **solo su mobile/tablet**
(< lg). Struttura consigliata: semplici `<li>` con `nav-link`:

```django
{% block offcanvas_nav %}
  <li><a href="/" class="nav-link active">{% bs_icon "house-fill" %} Home</a></li>
  <li><a href="/eventi/" class="nav-link">{% bs_icon "calendar-event" %} Eventi</a></li>
{% endblock %}
```

---

### `header_search`

Campo di ricerca nella barra inferiore dell'header, posizionato a sinistra.
Vuoto di default (la barra inferiore non viene nascosta ma rimane libera).

```django
{% block header_search %}
  <form class="col-12 col-lg-auto me-lg-auto" role="search">
    <input type="search" class="form-control" placeholder="Cerca..." aria-label="Cerca">
  </form>
{% endblock %}
```

---

### `header_actions`

Pulsanti o link nella barra inferiore, posizionati a destra.

```django
{% block header_actions %}
  <a href="{% url 'login' %}" class="btn btn-light text-dark">Accedi</a>
  <a href="{% url 'register' %}" class="btn btn-primary">Registrati</a>
{% endblock %}
```

---

## Blocco sidebar

### `sidebar`

Vuoto di default → layout a colonna singola. Quando viene popolato, appare
una colonna laterale a sinistra del `<main>`. Il modo più semplice è includere
il partial dedicato:

```django
{% block sidebar %}
  {% include "agesci_theme/partials/sidebar.html" with variant="dark" %}
{% endblock %}

{% block sidebar_items %}
  <li>
    <a href="/" class="ag-sidebar__nav-link {% if request.path == '/' %}active{% endif %}">
      <svg ...>...</svg>
      <span class="ag-sidebar__label">Home</span>
    </a>
  </li>
  <li>
    <a href="/impostazioni/" class="ag-sidebar__nav-link">
      <svg ...>...</svg>
      <span class="ag-sidebar__label">Impostazioni</span>
    </a>
  </li>
{% endblock %}
```

`variant` accetta `"dark"` (sfondo `--ag-primary`, default) oppure `"light"`
(sfondo chiaro con bordo).

Vedi [Sidebar](componenti.md#sidebar) per dettagli ed esempi.

---

## Blocchi del contenuto principale

### `main_class`

Classi CSS applicate al tag `<main>`. Default: `container py-4`.

```django
{# Tutta larghezza senza padding (es. mappa o dashboard) #}
{% block main_class %}container-fluid p-0{% endblock %}
```

---

### `messages`

Mostra i messaggi Django come alert Bootstrap 5. Raramente va sovrascritto.

```django
{% block messages %}{% endblock %}  {# nasconde tutti i messaggi #}
```

---

### `content`

**Blocco principale**: qui va il contenuto della pagina.

```django
{% block content %}
  <h1>Titolo pagina</h1>
  <p>Contenuto...</p>
{% endblock %}
```

---

## Blocchi del footer

### `footer`

Sostituisce l'intero footer.

```django
{% block footer %}
  {# footer completamente custom #}
{% endblock %}
```

---

### `footer_brand_text`

Breve testo mostrato sotto il logo nella colonna sinistra del footer.
Default: `agesci_theme_nome`.

```django
{% block footer_brand_text %}
  Zona Vesuvio — AGESCI Campania
{% endblock %}
```

---

### `footer_columns`

Blocco contenitore delle due colonne di link. Sovrascrivilo per aggiungere
più colonne o cambiarne la struttura.

```django
{% block footer_columns %}
  <div class="col-6 col-md-2">
    <h5>{% block footer_col1_title %}Sezione{% endblock %}</h5>
    <ul class="ag-footer__nav">{% block footer_col1_links %}{% endblock %}</ul>
  </div>
  <div class="col-6 col-md-2">
    <h5>{% block footer_col2_title %}Contatti{% endblock %}</h5>
    <ul class="ag-footer__nav">{% block footer_col2_links %}{% endblock %}</ul>
  </div>
{% endblock %}
```

---

### `footer_col1_title` / `footer_col2_title`

Titoli delle due colonne di link predefinite.

```django
{% block footer_col1_title %}Associazione{% endblock %}
{% block footer_col2_title %}Risorse{% endblock %}
```

---

### `footer_col1_links` / `footer_col2_links`

Voci `<li>` nelle due colonne di link.

```django
{% block footer_col1_links %}
  <li><a href="/chi-siamo/">Chi siamo</a></li>
  <li><a href="/branche/">Le branche</a></li>
{% endblock %}

{% block footer_col2_links %}
  <li><a href="https://www.agesci.it" target="_blank" rel="noopener">agesci.it</a></li>
  <li><a href="/documenti/">Documenti</a></li>
{% endblock %}
```

---

### `footer_text`

Testo nella colonna centrale del footer. Mantenuto dalla v1 per compatibilità.

```django
{% block footer_text %}
  <strong>Zona Vesuvio</strong><br>
  AGESCI Campania
{% endblock %}
```

---

### `footer_copyright`

Testo del copyright nella riga in fondo al footer. Default: `© AGESCI Campania`.

```django
{% block footer_copyright %}© {{ year }} Zona Vesuvio{% endblock %}
```

---

### `footer_links`

Link legali nella riga in fondo al footer (a destra del copyright).

```django
{% block footer_links %}
  <li><a href="/privacy/">Privacy</a></li>
  <li><a href="/accessibilita/">Accessibilità</a></li>
{% endblock %}
```

---

## Blocchi testa e coda

### `extra_head`

Inserisce contenuto alla fine del `<head>`.

```django
{% block extra_head %}
  <link rel="stylesheet" href="{% static 'mia_app/css/custom.css' %}">
{% endblock %}
```

---

### `extra_js`

Inserisce script prima di `</body>`, dopo Bootstrap JS.

```django
{% block extra_js %}{{ block.super }}
  <script src="{% static 'mia_app/js/custom.js' %}"></script>
{% endblock %}
```

Usa `{{ block.super }}` per mantenere eventuali script già definiti da blocchi
parent (es. la libreria Masonry quando usi `ag_masonry_grid`).

---

## Tabella riepilogativa

| Blocco | Posizione | Caso d'uso tipico |
|---|---|---|
| `title` | `<title>` | Titolo pagina |
| `extra_head` | fine `<head>` | CSS, meta aggiuntivi |
| `header` | intera testata | Sostituzione completa |
| `brand_url` | link brand | URL homepage custom |
| `brand_text` | nome brand | Nome sezione/zona |
| `header_nav` | nav desktop (con icone) | Voci menu desktop |
| `offcanvas_nav` | nav mobile offcanvas | Voci menu mobile |
| `header_search` | barra inferiore — sx | Campo di ricerca |
| `header_actions` | barra inferiore — dx | Pulsanti login/azioni |
| `sidebar` | colonna laterale sx | Sidebar collapsible |
| `main_class` | classi `<main>` | Layout a tutta larghezza |
| `messages` | sopra content | Nascondere i flash |
| `content` | corpo pagina | **Contenuto principale** |
| `footer` | fondo pagina | Sostituzione completa |
| `footer_brand_text` | colonna logo footer | Testo sotto il logo |
| `footer_columns` | colonne link footer | Struttura colonne |
| `footer_col1_title` | titolo colonna 1 | Nome sezione |
| `footer_col1_links` | link colonna 1 | `<li>` link |
| `footer_col2_title` | titolo colonna 2 | Nome sezione |
| `footer_col2_links` | link colonna 2 | `<li>` link |
| `footer_text` | testo centrale footer | Nome / slogan |
| `footer_copyright` | riga copyright | Anno e nome |
| `footer_links` | link legali footer | Privacy, contatti |
| `extra_js` | fine `<body>` | Script custom |

---

## Migrazione dalla v1.x

I blocchi rimossi nella v2 e il loro equivalente:

| Blocco v1 (rimosso) | Equivalente v2 |
|---|---|
| `navbar` | `header` |
| `nav_items` | `header_nav` + `offcanvas_nav` |
| `brand_url` | `brand_url` (invariato, ora in `header.html`) |
| `brand_text` | `brand_text` (invariato, ora in `header.html`) |
| `breadcrumb` | passare `breadcrumb_items` dal contesto della view (resa automaticamente in `ag-header-bottom`) oppure `{% ag_breadcrumb %}` nel blocco `content` |
| `subnav` | tag personalizzato nel blocco `content` |
